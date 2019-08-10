from rest_framework.views import APIView
from rest_framework.response import Response
from jobs.services.JobsApi.serializers import TechnologiesSerializer


class TechnologiesView(APIView):
    serializer=TechnologiesSerializer()

    def get(self,request):
        return Response({"tags":self.serializer.get()})
