from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from api.Models.BookingData import BookingData
from api.Models.ParkingLotDetails import ParkingLotDetails
from api.Serializers.BookingDataSerializer import BookingDataSerializer
from api.Serializers.ParkingLotDetailsSerializer import ParkingLotDetailsSerializer
from BizLogic.ParkingHistoryLogic import parkingHistoryAggregation
from logging import getLogger
from urllib.error import HTTPError
from Utils.UtilCommon import saveServerResponse
import json

logger = getLogger(__name__)

class ParkingHistoryView(APIView):
    def get(self,request:Request):
        try:
            logger.info("Received parking history request")
            response = {'error': ''}
            if 'user_id' in request.query_params.keys():
                userId = request.query_params.get('user_id')
                userParkingHistory = BookingData.objects.filter(user_id = userId)
                parkingHistorySerializer = BookingDataSerializer(userParkingHistory,many=True)
                if len(parkingHistorySerializer.data) > 0:
                    parkingLotDetails = ParkingLotDetails.objects.all()
                    parkingLotSerializer = ParkingLotDetailsSerializer(parkingLotDetails,many=True)
                    parkingHistory  = parkingHistoryAggregation(parkingHistorySerializer.data,parkingLotSerializer.data)
                    return JsonResponse(json.loads(parkingHistory),safe=False)
                else:
                    return Response({'records': len(parkingHistorySerializer.data)},status=status.HTTP_200_OK)
            response['error'] = 'Resource requires user_id parameter'
            saveServerResponse(request,'parking_history',response)
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        except HTTPError as err:
            errorResponse = {"error" : err.reason}
            saveServerResponse(request,'parking_history',errorResponse)
            return Response(errorResponse,status=err.code)
        except Exception as err:
            logger.exception(err)
            return Response(None,status=status.HTTP_500_INTERNAL_SERVER_ERROR)