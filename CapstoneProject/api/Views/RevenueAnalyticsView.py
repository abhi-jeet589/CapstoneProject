from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from api.Models.RevenueAnalyticsData import RevenueAnalyticsData
from api.Serializers.RevenueAnalyticsSerializer import RevenueAnalyticsSerializer
from logging import getLogger
from urllib.error import HTTPError
from datetime import date
from Utils.UtilCommon import saveServerResponse

logger = getLogger(__name__)

class RevenueAnalyticsView(APIView):
    def get(self,request:Request):
        try:
            logger.info("Received revenue analytics request")
            if request.query_params.get("date") is not None:
                filterDate = request.query_params.get("date")
            else:
                filterDate = date.today()
            revenueAnalytics = RevenueAnalyticsData.objects.filter(date_processed=filterDate)
            serializer = RevenueAnalyticsSerializer(revenueAnalytics,many=True)
            if len(serializer.data) > 0:
                saveServerResponse(request,'revenue_analytics',serializer.data[0])
                return JsonResponse(serializer.data[0],safe=False)
            notFoundResponse = {'error' : f'No data exists for date {filterDate}'}
            saveServerResponse(request,'revenue_analytics',notFoundResponse)
            return Response(notFoundResponse,status=status.HTTP_200_OK)
        except HTTPError as err:
            errorResponse = {"error" : err.reason}
            saveServerResponse(request,'revenue_analytics',errorResponse)
            return Response(errorResponse,status=err.code)
        except Exception as err:
            logger.exception(err)
            return Response(None,status=status.HTTP_500_INTERNAL_SERVER_ERROR)