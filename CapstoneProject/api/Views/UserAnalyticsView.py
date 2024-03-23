from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from api.Models.UserAnalyticsData import UserAnalyticsData
from api.Serializers.UserAnalyticsSerializer import UserAnalyticsSerializer
from BizLogic.UserAnalytics import userDetails
from logging import getLogger
from urllib.error import HTTPError
from rest_framework.views import APIView
from Utils.UtilCommon import saveServerResponse


logger = getLogger(__name__)

class UserAnalyticsView(APIView):
    def get(self,request:Request):
        try:
            logger.info("Received user analytics request")
            errorResponse = {'error': ''}
            if "date" in request.query_params.keys():
                filterDate = request.query_params.get("date")
                userAnalytics = UserAnalyticsData.objects.filter(date_processed=filterDate)
                serializer = UserAnalyticsSerializer(userAnalytics,many=True)
                if len(serializer.data) > 0:
                    saveServerResponse(request,'user_analytics',serializer.data[0])
                    return JsonResponse(serializer.data[0],safe=False)
                errorResponse['error'] = f'No data exists for date {filterDate}'
                saveServerResponse(request,'user_analytics',errorResponse)
                return Response(errorResponse,status=status.HTTP_200_OK)
            elif "filter" in request.query_params.keys():
                if request.query_params.get('filter') == "monthly":
                    if "year" in request.query_params.keys():
                        yearVal = request.query_params.get('year')
                        yearlyUserAnalytics = UserAnalyticsData.objects.filter(date_processed__year=yearVal)
                        yearlyData = UserAnalyticsSerializer(yearlyUserAnalytics,many=True)
                        yearlyUserResponse = {'January': 0,'February':0,'March':0,'April':0,'May':0,'June':0,'July':0,'August':0,'September':0,'October':0,'November':0,'December':0}
                        if len(yearlyData.data) > 0:
                            yearlyUserResponse= userDetails(yearlyData.data)
                            saveServerResponse(request,'user_analytics',yearlyUserResponse)
                            return Response(yearlyUserResponse,status=status.HTTP_200_OK)
                        saveServerResponse(request,'user_analytics',yearlyUserResponse)
                        return Response(yearlyUserResponse,status=status.HTTP_200_OK)
                    errorResponse['error'] = 'The filter query parameter requires a year value.'
                    saveServerResponse(request,'user_analytics',errorResponse)
                    return Response(errorResponse,status=status.HTTP_400_BAD_REQUEST)
            else:
                errorResponse['error'] = 'Endpoint requires query parameter'
                saveServerResponse(request,'user_analytics',errorResponse)
                return Response(errorResponse,status=status.HTTP_400_BAD_REQUEST)
        except HTTPError as err:
            errorResponse = {"error" : err.reason}
            saveServerResponse(request,'user_analytics',errorResponse)
            return Response(errorResponse,status=err.code)
        except Exception as err:
            logger.exception(err)
            return Response(None,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
