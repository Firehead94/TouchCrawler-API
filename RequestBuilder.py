import json
from firebase_admin import credentials, firestore
import time
import firebase_admin
from enum import Enum
import typing


class RequestBuilder:

    def __init__(self, data, error: typing.Optional = None):
        self.data = data
        self.error = error

    def get_request(self):
        request = gettemplate()
        if self.data is not None:
            request["data"] = self.data
        else:
            request["error"] = errors[Error.DATA.value]
        if self.error is not None:
            request["error"] = errors[self.error.value]
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