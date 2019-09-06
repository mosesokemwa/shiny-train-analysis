from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from jobs.services.JobsApi.serializers import JobLocationsSerializer


class JobsLocationView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self,request):
        serializer = JobLocationsSerializer()
        data = serializer.get(request.GET)
        return Response(data)
        