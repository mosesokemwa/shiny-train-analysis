from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from jobs.services.JobsApi.serializers import JobsApiSerializer


class JobsView(APIView):
    permission_classes = [IsAuthenticated,]
    serializer=JobsApiSerializer()
    def get(self,request):
        return Response(self.serializer.filter(request.GET))