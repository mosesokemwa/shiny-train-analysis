from rest_framework.views import APIView
from rest_framework.response import Response

from jobs.services.JobsApi.serializers import ProvidersSerializer

class ProvidersViews(APIView):

    def get(self,request):
        serializer = ProvidersSerializer()
        data = serializer.get(request.GET)
        return Response(data)