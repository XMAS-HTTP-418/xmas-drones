from dataclasses import dataclass
from json import JSONDecoder, JSONEncoder


class SlaveInfo:
    def __init__(self, rawClientInfo):
        self.connection = rawClientInfo[0]
        rawAddress = rawClientInfo[1]
        self.ipAddress = rawAddress[0]
        self.port = rawAddress[1]
        self.fullAddress = f"{self.ipAddress}:{self.port}"


class Request:
    def __init__(self, controller, action, body=None):
        self.controller = controller
        self.action = action
        self.body = body

    @staticmethod
    def from_Json(requestJson):
        jsonRequest = JSONDecoder().decode(requestJson)
        controller = jsonRequest["controller"]
        action = jsonRequest["action"]
        body = jsonRequest["body"]
        return Request(controller, action, body)

    def toJson(self):
        requestDict = {
            "controller": self.controller,
            "action": self.action,
            "body": self.body,
        }
        requestJson = JSONEncoder().encode(requestDict)
        return requestJson


class Response:
    def __init__(self, succeed: bool, errorMessage: str, body: dict = None, changes: bool = False):
        self.changes = changes
        self.body = body
        self.errorMessage = errorMessage
        self.succeed = succeed

    def toJson(self):
        responseDict = {
            "succeed": self.succeed,
            "errorMessage": self.errorMessage,
            "changes": self.changes,
            "body": self.body,
        }
        responseJson = JSONEncoder().encode(responseDict)
        return responseJson

    @staticmethod
    def from_json(responseJson):
        jsonResponse = JSONDecoder().decode(responseJson)
        body = jsonResponse["body"]
        errorMessage = jsonResponse["errorMessage"]
        succeed = jsonResponse["succeed"]
        changes = jsonResponse["changes"]
        return Response(succeed, errorMessage, body, changes)
