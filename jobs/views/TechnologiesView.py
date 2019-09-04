from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from jobs.services.JobsApi.serializers import TechnologiesSerializer
from jobs.services.oauth_providers.canvas_oauth.authentication import CanvasAuthentication
from jobs.services.oauth_providers.google_oauth2.authentication import GoogleOauth2Authentication


class TechnologiesView(APIView):
    serializer=TechnologiesSerializer()
    authentication_classes = [CanvasAuthentication,GoogleOauth2Authentication]
    permission_classes = [IsAuthenticated,]

    def get(self,request):
        return Response({"tags":self.serializer.get()})
