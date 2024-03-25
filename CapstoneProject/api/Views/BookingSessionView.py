from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from api.Models.BookingSession import BookingSession
from api.Serializers.BookingSessionSerializer import BookingSessionSerializer
from logging import getLogger
from urllib.error import HTTPError
from Utils.UtilCommon import saveServerResponse


logger = getLogger(__name__)

class BookingSessionView(APIView):
    def get(self,request:Request):
        try:
            logger.info("Received booking session info request")
            response = {'error': ''}
            if 'booking_id' in request.query_params.keys():
                bookingId = request.query_params.get('booking_id')
                bookingHistory = BookingSession.objects.filter(booking_id = bookingId)
                bookingHistorySerializer = BookingSessionSerializer(bookingHistory,many=True)
                if len(bookingHistorySerializer.data) > 0:
                    return JsonResponse(bookingHistorySerializer.data[0],safe=False)
                else:
                    return Response({'records': len(bookingHistorySerializer.data)},status=status.HTTP_200_OK)
            response['error'] = 'Resource requires booking_id parameter'
            saveServerResponse(request,'booking_history',response)
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        except HTTPError as err:
            errorResponse = {"error" : err.reason}
            saveServerResponse(request,'booking_history',errorResponse)
            return Response(errorResponse,status=err.code)
        except Exception as err:
            logger.exception(err)
            return Response(None,status=status.HTTP_500_INTERNAL_SERVER_ERROR)