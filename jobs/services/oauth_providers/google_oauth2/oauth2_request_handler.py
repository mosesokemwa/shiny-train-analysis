from  jobs.services.oauth_providers.abstract_oauth2_request_handler import AbstractOauth2RequestHandler
import json, base64
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import exceptions
from .models import GoogleOuth2AccessToken

class GoogleOuth2RequestHandler(AbstractOauth2RequestHandler):
    
    def __init__(self, *args, **kwargs):
        self.CLIENT_ID = settings.GOOGLE_CLIENT_ID
        self.CLIENT_SECRET =  settings.GOOGLE_CLIENT_SECRET
        self.CLIENT_REDIRECT_URI = settings.GOOGLE_REDIRECT_URI

    def get_access_token(self, code):
        print(code)
        endpoint="https://oauth2.googleapis.com/token?access_type=offline"
        data={
            "grant_type":"authorization_code",
            "client_id":self.CLIENT_ID,
            "client_secret":self.CLIENT_SECRET,
            "redirect_uri":self.CLIENT_REDIRECT_URI,
            "code":code
        }
        data = self.make_request("post",endpoint,{"data":data})
        data["user"] =  self.decode_jwt(data["id_token"])
        try:
            token = self.create_update_user(data)
            return token
        except Exception as e:
            print(str(e))
            raise exceptions.APIException("Server Error check logs")
   
    def decode_jwt(self, id_token):
        try:
            return json.loads(base64.decodestring(id_token.split('.')[1].encode()).decode())
        except Exception as e:
            raise exceptions.APIException("Unable to decode jwt")

    def create_update_user(self, data):
        try:
            google_token = GoogleOuth2AccessToken.objects.get(email= data["user"]["email"])
        except GoogleOuth2AccessToken.DoesNotExist:
            google_token = GoogleOuth2AccessToken(email=data["user"]["email"])
            user,_ = User.objects.get_or_create(username=data["user"]["email"])
            user.first_name = data["user"]["given_name"]
            user.save()
            google_token.user = user
        google_token.access_token = data["access_token"]
        if "refresh_token" in data:
            google_token.refresh_token = data["refresh_token"]
        google_token.expires = timezone.now() + timedelta(seconds=data['expires_in'])
        google_token.save()
        return google_token.access_token
