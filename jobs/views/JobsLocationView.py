from rest_framework.views import APIView
from rest_framework.response import Response

from jobs.services.JobsApi.serializers import JobLocationsSerializer


class JobsLocationView(APIView):

    def get(self,request):
        serializer = JobLocationsSerializer()
        data = serializer.get(request.GET)
        return Response(data)
        