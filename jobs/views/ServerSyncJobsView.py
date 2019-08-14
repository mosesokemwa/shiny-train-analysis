from rest_framework.views import APIView
from rest_framework.response import Response
from jobs.services.JobsApi.serializers import SyncJobsSerializer


class ServerSyncJobsView(APIView):

    def get(self,request):
        serializer = SyncJobsSerializer()
        data = serializer.get(request.GET)
        return Response(data)