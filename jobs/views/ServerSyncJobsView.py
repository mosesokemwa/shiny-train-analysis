from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from jobs.services.JobsApi.serializers import SyncJobsSerializer


class ServerSyncJobsView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        serializer = SyncJobsSerializer()
        data = serializer.get(request.GET)
        return Response(data)