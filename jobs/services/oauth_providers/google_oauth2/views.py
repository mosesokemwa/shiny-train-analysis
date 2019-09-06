from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .oauth2_request_handler import GoogleOuth2RequestHandler

google_oauth2_handler = GoogleOuth2RequestHandler()

class GoogleOauth2LoginApiView(APIView):
    permission_classes = [AllowAny,]
    def get(self, request):
        code  = request.GET.get("code",None)
        if code != None:
            token=google_oauth2_handler.get_access_token(code)
            return Response({"token":token}, status.HTTP_200_OK)
        return Response({"error":"Bad request"},status.HTTP_400_BAD_REQUEST)
