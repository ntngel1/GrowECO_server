from flask import jsonify
import datetime
import secrets

from server import models
from server.exceptions import *
from server.datapreprocessor import *

ERROR_CODE = 400


def error_response(data=None):
    if data is None:
        return jsonify({'success': False}), ERROR_CODE
    else:
        data.update({'success': False})
        return jsonify(data), ERROR_CODE


def success_response(data=None):
    if data is None:
        return jsonify({'success': True})
    else:
        data.update({'success': True})
        return jsonify(data)


def create_user(request_data):
    try:
        registration_data = RequestDataPreprocessor.create_user_data(request_data)
    except ServerErrorException as e:
        return error_response(e.get_dict())

    try:
        models.create_user(registration_data)
    except ServerErrorException as e:
        return error_response(e.get_dict())

    return success_response()


def get_user(username):
    user = models.get_user(username)
    response = ResponseDataPreprocessor.get_user_data(user)
    return success_response(response)


def update_user(username, request_data):
    update_data = RequestDataPreprocessor.update_user_data(request_data)
    models.update_user(username, update_data)
    return success_response()


def get_sensors(token):
    try:
        sensors = models.get_sensors(token)
    except ServerErrorException as e:
        return error_response(e.get_dict())

    response = ResponseDataPreprocessor.get_sensors_data(sensors)
    return success_response(response)


def update_sensors(token, request_data):
    update_data = RequestDataPreprocessor.update_sensors_data(request_data)

    try:
        models.update_sensors(token, update_data)
    except ServerErrorException as e:
        return error_response(e.get_dict())

    return success_response()


def get_device_slot(owner):
    slot = models.get_device_slot(owner)
    response = ResponseDataPreprocessor.get_device_slot(slot)
    return success_response(response)


def attach_device(token):
    new_token = str(secrets.token_hex(16))

    try:
        response = models.update_device(token, {'token': new_token, 'is_attached': True,
                                                'last_online': datetime.datetime.utcnow()})
    except ServerErrorException as e:
        return error_response(e.get_dict())

    response = ResponseDataPreprocessor.attach_device(response)

    return success_response(response)


def get_devices(username):
    devices = models.get_devices(username)

    response = dict()
    response['devices'] = list()
    for device in devices:
        device = ResponseDataPreprocessor.get_device(device)
        response['devices'].append(device)

    return success_response(response)


def update_device(token, data):
    update_data = RequestDataPreprocessor.update_device_data(data)
    try:
        models.update_device(token, update_data)
    except ServerErrorException as e:
        return error_response(e.get_dict())

    return success_response()

def create_action(token, data):
   action_data = RequestDataPreprocessor.create_action(data)

   try:
       models.create_action(token, action_data)
   except ServerErrorException as e:
       return error_response(e.get_dict())

   return success_response()


def get_action(token):
   try:
       action = models.get_action(token)
       return success_response(action)
   except ServerErrorException as e:
       return error_response(e.get_dict())

