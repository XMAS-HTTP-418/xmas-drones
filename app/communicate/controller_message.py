
from typing import Callable
from communicate.models import Request, Response
from logger import Logger



class MessageController:

    def __init__(self, clientIndex, message_callback: Callable = lambda _:_):
        self.clientIndex = clientIndex
        self.currentController = None
        self.message_callback = message_callback

    # TODO здесь парсим и раскидваем request
    def handle(self, requestData) -> Response:
        request = Request.from_Json(requestData)
        Logger.log(f"Slave #{self.clientIndex} requested {request.controller}/{request.action}")
        if self.message_callback:
            return self.message_callback(requestData) # требуется для создания коллбеков у дронов
        else:
            return Response(True,"dsa",{"das": "das"}) # старый функционал