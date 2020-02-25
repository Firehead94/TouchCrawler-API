import json
from firebase_admin import credentials, firestore
import time
import firebase_admin
from enum import Enum


class RequestBuilder:

    def buildrequest(self, data, error):
        request = self.gettemplate()
        if data is not None:
            request["data"] = data
        else:
            request["error"] = Error.DATA
        if error is not None:
            request["error"] = error
        return request

    def gettemplate(self):
        request = {}
        request["error"] = None
        request["timestamp"] = time.asctime(time.localtime(time.time()))
        request["data"] = {}
        return request


class Error(Enum):
    DATA = "1001: No Data Found"
    API = "1002: Invalid API Request"
    TOKEN = "1003: Bad/Expired Token"
    DOCUMENT = "1004: No Document Found"
    UID = "1005: User Not Found"