from api.Models.RequestStore import RequestStore
from json import dumps
from rest_framework.reverse import reverse

def saveServerResponse(incomingRequest,viewname:str,outgoingResponse) -> None:
    try:
        requestStoreObj = RequestStore(request=reverse(viewname=viewname,request=incomingRequest),response=dumps(outgoingResponse,default=int))
        requestStoreObj.save()
    except Exception:
        raise Exception("Unable to store request in Database")   