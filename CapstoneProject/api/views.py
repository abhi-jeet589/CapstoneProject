from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework import status
from Utils import UtilConnection
from BizLogic.AnalyticsLogic import parkingDetails
from .models import RequestStore
from json import dumps
import logging
from urllib.error import HTTPError


DBConnect = UtilConnection.DBConnect()
DBConnect.connectDb()
firebaseDb = DBConnect.getDb()
logger = logging.getLogger(__name__)

def saveServerResponse(incomingRequest,viewname:str,outgoingResponse) -> None:
    try:
        requestStoreObj = RequestStore(request=reverse(viewname=viewname,request=incomingRequest),response=dumps(outgoingResponse))
        requestStoreObj.save()
    except Exception:
        logger.error("Unable to store request in Database")   

@api_view(['GET'])
def parking(request:Request):
    try:
        logger.info("Received request")
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
