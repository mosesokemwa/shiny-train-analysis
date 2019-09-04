from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class UserView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        user =  request.user
        res={
            "id":user.id,
            "short_name":user.first_name
        }
        return Response(res,status.HTTP_200_OK)
