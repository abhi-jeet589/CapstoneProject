from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from api.Models.UserModel import UserModel
from api.Serializers.UserModelSerializer import UserModelSerializer
from logging import getLogger
from urllib.error import HTTPError
from Utils.UtilCommon import saveServerResponse


logger = getLogger(__name__)

class UserView(APIView):
    def get(self,request:Request):
        try:
            logger.info("Received user info request")
            response = {'error': ''}
            if 'user_id' in request.query_params.keys():
                userId = request.query_params.get('user_id')
                userObjects = UserModel.objects.filter(user_id = userId)
                serializer = UserModelSerializer(userObjects,many=True)
                if len(serializer.data) > 0:
                    return JsonResponse(serializer.data[0],safe=False)
                else:
                    response['error'] = 'User does not exist'
                    saveServerResponse(request,'user_info',response)
                    return Response(response,status=status.HTTP_404_NOT_FOUND)
            response['error'] = 'Resource requires user_id parameter'
            saveServerResponse(request,'user_info',response)
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        except HTTPError as err:
            errorResponse = {"error" : err.reason}
            saveServerResponse(request,'user_info',errorResponse)
            return Response(errorResponse,status=err.code)
        except Exception as err:
            logger.exception(err)
            return Response(None,status=status.HTTP_500_INTERNAL_SERVER_ERROR)