from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from Utils import UtilConnection
from BizLogic.ParkingAnalytics import parkingDetails
from Utils.UtilCommon import saveServerResponse
import logging
from urllib.error import HTTPError
from rest_framework.views import APIView

DBConnect = UtilConnection.DBConnect()
DBConnect.connectDb()
firebaseDb = DBConnect.getDb()
logger = logging.getLogger(__name__)

class ParkingView(APIView):
    def get(self,request):
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
            logger.info(response)
            saveServerResponse(request,'parking',response)
            return Response(response,status=status.HTTP_200_OK)
        except HTTPError as err:
            errorResponse = {"error" : err.reason}
            saveServerResponse(request,'parking',errorResponse)
            return Response(errorResponse,status=err.code)
        except Exception as err:
            logger.exception(err)
            return Response(None,status=status.HTTP_500_INTERNAL_SERVER_ERROR)







