from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .canvas_oauth2_request_handler import CanvasOauth2RequestHandler

canvas_oauth_handler = CanvasOauth2RequestHandler()

class CanvasLoginApiView(APIView):
    permission_classes = [AllowAny]
    def get(self,request,*args, **kwargs):
        code =request.GET.get("code",None)
        if code  != None:
            token=canvas_oauth_handler.oauth_token(code)
            return Response({"token":token}, status.HTTP_200_OK)
        return Response({"error":"Bad request"},status.HTTP_400_BAD_REQUEST)