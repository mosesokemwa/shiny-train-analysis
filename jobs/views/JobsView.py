from rest_framework.views import APIView
from rest_framework.response import Response

from jobs.services.JobsApi.serializers import JobsApiSerializer


class JobsView(APIView):
    serializer=JobsApiSerializer()
    def get(self,request):
        return Response(self.serializer.filter(request.GET))