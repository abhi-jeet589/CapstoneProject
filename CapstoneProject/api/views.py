from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from Utils import UtilConnection
from BizLogic.AnalyticsLogic import parkingDetails

DBConnect = UtilConnection.DBConnect()
DBConnect.connectDb()
firebaseDb = DBConnect.getDb()


@api_view(['GET'])
def parking(request:Request):
    try:
        if request.query_params.get("location") is not None:
            toplevelChild = request.query_params.get("location")
            locationData = firebaseDb.get(toplevelChild).val()
        else:
            locationData = firebaseDb.get().val()
        return Response(parkingDetails(locationData),status=status.HTTP_200_OK)
          
    except Exception as err:
        print(err)
        return Response(None,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
