from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import RequestStore
from .serializers import RequestStoreSerializer


@api_view(['POST'])
def index(request:Request):
    if request.data:
        res = {'Response':'everything good'}
        try:
            RequestStore.objects.create(request=request.data,response=res).save()
        except Exception as err:
            return Response({'Unable to save to DB'},status=status.HTTP_400_BAD_REQUEST)
    return Response({'Saved to DB'},status=status.HTTP_200_OK)

    
