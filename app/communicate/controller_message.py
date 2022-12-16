

from communicate.models import Request, Response
from logger import Logger



class MessageController:

    def __init__(self, clientIndex):
        self.clientIndex = clientIndex
        self.currentController = None


    def handle(self, requestData) -> Response:
        request = Request.from_Json(requestData)
        Logger.log(f"Client #{self.clientIndex} requested {request.controller}/{request.action}")
        return Response(True,"dsa",{"sam": "takoy"}, False)