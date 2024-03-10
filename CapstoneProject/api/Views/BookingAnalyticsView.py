from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from api.Models.BookingData import BookingData
from api.Serializers.BookingDataSerializer import BookingDataSerializer
from logging import getLogger
from urllib.error import HTTPError
from datetime import date
from Utils.UtilCommon import saveServerResponse


logger = getLogger(__name__)
year_dict = {1: 'January',2 : 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}


class BookingAnalyticsView(APIView):
    
    def get(self,request:Request):
        try:
            logger.info("Received booking analytics request")
            if "filter" in request.query_params.keys():
                if request.query_params.get('filter') == "monthly":
                    if "year" in request.query_params.keys():
                        yearVal = request.query_params.get('year')
                        yearlyBookingAnalytics = BookingData.objects.filter(booking__year=yearVal)
                        yearlyBookingResponse = {}
                        for month_number, month_name in year_dict.items():
                            monthlyBookingAnalytics = yearlyBookingAnalytics.filter(booking__month=month_number)
                            serializer = BookingDataSerializer(monthlyBookingAnalytics,many=True)
                            yearlyBookingResponse[month_name] = len(serializer.data)
                        return JsonResponse(yearlyBookingResponse,safe=False)
                    return Response({'error': 'The filter query parameter requires a year value.'},status=status.HTTP_400_BAD_REQUEST)
                elif request.query_params.get('filter') == "weekly":
                    weeklyBookingResponse = {}
                    current_year,current_week,current_day_of_week = date.today().isocalendar()
                    weeklyBookingAnalytics = BookingData.objects.filter(booking__week = current_week)
                    serializer = BookingDataSerializer(weeklyBookingAnalytics,many=True)
                    weeklyBookingResponse['current_week'] = len(serializer.data)
                    prevWeeklyBookingAnalytics = BookingData.objects.filter(booking__week = current_week - 1)
                    serializer = BookingDataSerializer(prevWeeklyBookingAnalytics,many=True)
                    weeklyBookingResponse['prev_week'] = len(serializer.data)
                    weeklyBookingResponse['pct_change'] = "{:.2f}".format(((weeklyBookingResponse['current_week']/weeklyBookingResponse['prev_week']) - 1)*100)
                    return JsonResponse(weeklyBookingResponse,safe=False)
                else:
                    return Response({'error' : 'Malformed request'},status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Endpoint requires query parameter'},status=status.HTTP_400_BAD_REQUEST)
        except HTTPError as err:
            errorResponse = {"error" : err.reason}
            saveServerResponse(request,'booking_analytics',errorResponse)
            return Response(errorResponse,status=err.code)
        except Exception as err:
            logger.exception(err)
            return Response(None,status=status.HTTP_500_INTERNAL_SERVER_ERROR)