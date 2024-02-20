from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework import status
from Utils import UtilConnection
from BizLogic.AnalyticsLogic import parkingDetails
from .models import RequestStore
from json import dumps
from Utils.UtilLogger import UtilLogger


DBConnect = UtilConnection.DBConnect()
DBConnect.connectDb()
firebaseDb = DBConnect.getDb()


@api_view(['GET'])
def parking(request:Request):
    logger = UtilLogger(__name__).getlogger()
    try:
        logger.info("Received request")
        if request.query_params.get("location") is not None:
            toplevelChild = request.query_params.get("location")
            if firebaseDb.child(toplevelChild).shallow().get().val() is None:
                return Response({"error" : "Parking lot not found"},status=status.HTTP_404_NOT_FOUND)
            locationData = {toplevelChild: firebaseDb.child(toplevelChild).get().val()}
        else:
            locationData = firebaseDb.get().val()
        response = parkingDetails(locationData)
        try:
            requestStoreObj = RequestStore(request=reverse(viewname='parking',request=request),response=dumps(response))
            requestStoreObj.save()
            logger.info("saved to db")
        except Exception as err:
            print(err)
            return Response(None,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(response,status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return Response(None,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
