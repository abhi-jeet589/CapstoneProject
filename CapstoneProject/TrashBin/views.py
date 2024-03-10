from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework import status
from Utils import UtilConnection
from BizLogic.ParkingAnalytics import parkingDetails
from api.models import RequestStore,UserAnalyticsData,BookingData
from api.serializers import UserAnalyticsSerializer,BookingDataSerializer
from json import dumps
import logging
from urllib.error import HTTPError
from datetime import date



DBConnect = UtilConnection.DBConnect()
DBConnect.connectDb()
firebaseDb = DBConnect.getDb()
logger = logging.getLogger(__name__)
year_dict = {1: 'January',2 : 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

def saveServerResponse(incomingRequest,viewname:str,outgoingResponse) -> None:
    try:
        requestStoreObj = RequestStore(request=reverse(viewname=viewname,request=incomingRequest),response=dumps(outgoingResponse))
        requestStoreObj.save()
    except Exception:
        logger.error("Unable to store request in Database")   

@api_view(['GET'])
def parking(request:Request):
    try:
        logger.info("Received parking analytics request")
        if request.query_params.get("location") is not None:
            toplevelChild = request.query_params.get("location")
            if toplevelChild not in firebaseDb.get().val().keys():
                logger.info(f"No top level child found in Database with name {toplevelChild}")
                raise HTTPError(url=reverse(viewname='parking',request=request),code=404,msg=f'Parking lot not found with name {toplevelChild}',hdrs=None,fp=None)
            locationData = {toplevelChild: firebaseDb.child(toplevelChild).get().val()}
        else:
            locationData = firebaseDb.get().val()
        response = parkingDetails(locationData)
        saveServerResponse(request,'parking',response)
        return Response(response,status=status.HTTP_200_OK)
    except HTTPError as err:
        errorResponse = {"error" : err.reason}
        saveServerResponse(request,'parking',errorResponse)
        return Response(errorResponse,status=err.code)
    except Exception as err:
        logger.exception(err)
        return Response(None,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def userAnalytics(request:Request):
    try:
        logger.info("Received user analytics request")
        if request.query_params.get("date") is not None:
            filterDate = request.query_params.get("date")
        else:
            filterDate = date.today()
        userAnalytics = UserAnalyticsData.objects.filter(date_processed=filterDate)
        serializer = UserAnalyticsSerializer(userAnalytics,many=True)
        if len(serializer.data) > 0:
            saveServerResponse(request,'user_analytics',serializer.data[0])
            return JsonResponse(serializer.data[0],safe=False)
        notFoundResponse = {'error' : f'No data exists for date {filterDate}'}
        saveServerResponse(request,'user_analytics',notFoundResponse)
        return Response(notFoundResponse,status=status.HTTP_404_NOT_FOUND)
    except HTTPError as err:
        errorResponse = {"error" : err.reason}
        saveServerResponse(request,'user_analytics',errorResponse)
        return Response(errorResponse,status=err.code)
    except Exception as err:
        logger.exception(err)
        return Response(None,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def bookingAnalytics(request:Request):
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