import json
from firebase_admin import credentials, firestore
import time
import firebase_admin
from enum import Enum
import typing


class RequestBuilder:

    def buildrequest(self, data, error: typing.Optional = None):
        request = gettemplate()
        print("data")
        print(data)
        print("error")
        print(error)
        if data is not None:
            request["data"] = data
        else:
            print("============no data==============")
            request["error"] = errors[Error.DATA.value]
        if error is not None:
            request["error"] = errors[error.value]
        return request


def gettemplate():
    request = {}
    request["error"] = None
    request["timestamp"] = time.asctime(time.localtime(time.time()))
    request["data"] = {}
    return request


class Error(Enum):
    DATA = 0
    API = 1
    TOKEN = 2
    DOCUMENT = 3
    UID = 4

errors = ["1001: No Data Found","1002: Invalid API Request","1003: Bad/Expired Token","1004: No Document Found","1005: User Not Found"]