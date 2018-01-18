from enum import IntEnum
from flask import jsonify


class ErrorCode(IntEnum):
    NULL = 0
    DEVICE_NOT_REGISTERED = 1
    DATA_NOT_SUITABLE = 2
    OTHER_ERROR = 3
    INVALID_DEVICE_TOKEN = 4


class ServerErrorException(Exception):
    def __init__(self, code=3, json=None, message=None, *args):
        Exception.__init__(self, *args)
        if json is None:
            json = {'error': {}}
        self.json = json
        self.json['error']['error_message'] = message
        self.json['error']['error_code'] = code

    def get_json(self):
        return jsonify(self.json)

    def get_dict(self):
        return self.json


class DataNotSuitableException(ServerErrorException):
    def __init__(self, errors=None, message="Некорректные данные!"):
        json = dict()
        if errors:
            json['error'] = errors
        ServerErrorException.__init__(self, ErrorCode.DATA_NOT_SUITABLE, json, message)


class InvalidDeviceTokenException(ServerErrorException):
    def __init__(self):
        ServerErrorException.__init__(self, ErrorCode.INVALID_DEVICE_TOKEN,
                                      message="Недействительный токен устройства!")
