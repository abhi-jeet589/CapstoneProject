from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from api.Models.UserAnalyticsData import UserAnalyticsData
from api.Serializers.UserAnalyticsSerializer import UserAnalyticsSerializer
from logging import getLogger
from urllib.error import HTTPError
from datetime import date
from rest_framework.views import APIView
from Utils.UtilCommon import saveServerResponse

logger = getLogger(__name__)


class UserAnalyticsView(APIView):
    def get(self,request:Request):
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
            return Response(notFoundResponse,status=status.HTTP_200_OK)
        except HTTPError as err:
            errorResponse = {"error" : err.reason}
            saveServerResponse(request,'user_analytics',errorResponse)
            return Response(errorResponse,status=err.code)
        except Exception as err:
            logger.exception(err)
            return Response(None,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
