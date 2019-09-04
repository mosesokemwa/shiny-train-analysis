from rest_framework import authentication
from rest_framework import exceptions, HTTP_HEADER_ENCODING
from django.contrib.auth.models import User
from .models import GoogleOuth2AccessToken

class GoogleOauth2Authentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).decode(HTTP_HEADER_ENCODING)
        auth = auth_header.split()
        if not auth or auth[0].lower() != 'bearer':
            return None
        elif len(auth) != 2:
            msg = 'Invalid token header.'
            raise exceptions.AuthenticationFailed(msg)
        token = auth[1]
        user = self.get_user(token)
        if not user:
            return None
        return user, token

    def get_user(self,token):
        # @todo check if token has expired
        try:
            google_token = GoogleOuth2AccessToken.objects.get(access_token = token)
            user = google_token.user
            return user
        except GoogleOuth2AccessToken.DoesNotExist:
            return None
        except Exception as e:
            print(str(e))
            return None

        
        