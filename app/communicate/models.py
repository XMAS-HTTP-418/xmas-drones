from json import JSONDecoder, JSONEncoder


class SlaveInfo:
    def __init__(self, raw_client_info):
        self.connection = raw_client_info[0]
        raw_address = raw_client_info[1]
        self.ip_address = raw_address[0]
        self.port = raw_address[1]
        self.full_address = f"{self.ip_address}:{self.port}"


class Request:
    def __init__(self, controller, action, body=None):
        self.controller = controller
        self.action = action
        self.body = body

    @staticmethod
    def from_Json(request_json):
        json_request = JSONDecoder().decode(request_json)
        controller = json_request["controller"]
        action = json_request["action"]
        body = json_request["body"]
        return Request(controller, action, body)

    def to_json(self):
        request_dict = {
            "controller": self.controller,
            "action": self.action,
            "body": self.body,
        }
        requestJson = JSONEncoder().encode(request_dict)
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


