import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.utils  import timezone
from datetime import timedelta
from .models import CanvasOauthToken
from rest_framework import exceptions
import json
from jobs.services.oauth_providers.abstract_oauth2_request_handler import AbstractOauth2RequestHandler


class CanvasOauth2RequestHandler(AbstractOauth2RequestHandler):

    def __init__(self,*args, **kwargs):
        self.CLIENT_SECRET= settings.CANVAS_SECRET
        self.CLIENT_ID= settings.CANVAS_CLIENTID
        self.CLIENT_ENDPOINT= settings.CANVAS_INSTANCE
        self.CLIENT_REDIRECT_URI= settings.CANVAS_REDIRECT

    def oauth_token(self,code):
        data={
            "grant_type":"authorization_code",
            "client_id":self.CLIENT_ID,
            "client_secret":self.CLIENT_SECRET,
            "redirect_uri":self.CLIENT_REDIRECT_URI,
            "code":code
        }
        print(data)
        data = self.make_request("post",self.CLIENT_ENDPOINT+"/login/oauth2/token",{"data":data})

        try:
            canvas_token=self.create_update_user(data)
        except Exception as e:
            message = str(e)
            print(message)
            raise exceptions.APIException("Server error: %s"%message)
        return canvas_token.access_token

    def refresh_token(self,token):
        try:
            canvas_token = CanvasOauthToken.objects.get(access_toke=token)
        except CanvasOauthToken.DoesNotExist:
            raise exceptions.APIException("Invalid Access Token")
        data={
            "grant_type":"refresh_token",
            "client_id":self.CLIENT_ID,
            "client_secret":self.CLIENT_SECRET,
            "refresh_token":canvas_token.refresh_token
        }
        data = self.make_request("post",self.CANVAS_INSTANCE+"/login/oauth2/token",{"data":data})
        try:
            canvas_token=self.create_update_user(data)
        except Exception as e:
            message = str(e)
            print(message)
            raise exceptions.APIException("Server error: %s"%message)
        return canvas_token.access_token

    def create_update_user(self,response):
        try:
            canvas_token = CanvasOauthToken.objects.get(canvas_id=str(response["user"]["id"]))
        except CanvasOauthToken.DoesNotExist:
            canvas_token = CanvasOauthToken()
            user,_ = User.objects.get_or_create(username=response["user"]["name"])
            # short name
            user.first_name = response["user"]["name"]
            user.save()
            canvas_token.user = user
        canvas_token.access_token = response['access_token']
        if "refresh_token" in response:
            canvas_token.refresh_token = response['refresh_token']
        canvas_token.expires=timezone.now() + timedelta(seconds=response['expires_in'])
        canvas_token.save()
        return canvas_token

