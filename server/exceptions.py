from enum import IntEnum
from flask import jsonify

class ErrorCode(IntEnum):
    NOT_OWNER = 0
    DEVICE_NOT_REGISTERED = 1
    DATA_NOT_SUITABLE = 2
    OTHER_ERROR = 3
    INVALID_DEVICE_TOKEN = 4


class ServerErrorException(Exception):
    def __init__(self, code=4, json=None, message=None, *args):
        Exception.__init__(self, *args)
        if json is None:
            json = dict()
        self.json = json
        self.json['error_message'] = message
        self.json['error_code'] = code

    def get_json(self):
        return jsonify(self.json)

    def get_dict(self):
        return self.json
