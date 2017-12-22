from flask import jsonify
from server import models
from server import exceptions
import datetime
import secrets
from bson.json_util import dumps


def register_account(req_data):
    params = ['name', 'username', 'password', 'email']
    new_user_data = {}

    errors = dict()

    if not req_data:
        return exceptions.ServerErrorException(exceptions.ErrorCode.DATA_NOT_SUITABLE,
                                               message="Данные отсутствуют!").get_json(), 400

    for param in params:
        if param in req_data:
            new_user_data[param] = req_data[param]
        else:
            errors[param] = "Значение не может отсутствовать!"

    if errors:
        return exceptions.ServerErrorException(exceptions.ErrorCode.DATA_NOT_SUITABLE,
                                               errors, "Некоторые данные отсутствуют!").get_json(), 400
    else:
        return do_with_handling(models.create_user, new_user_data)


def get_account(username):
    return do_with_handling(models.get_user, username)


def update_account(username, req_data):
    params = ['name', 'username', 'password', 'email']
    new_user_data = dict()

    if not req_data:
        return exceptions.ServerErrorException(exceptions.ErrorCode.DATA_NOT_SUITABLE,
                                               message="Данные отсутствуют!").get_json()
    for param in params:
        try:
            new_user_data[param] = req_data[param]
        except KeyError:
            continue

    return do_with_handling(models.update_user, username, new_user_data)


def get_sensors(username, device_id):
    return do_with_handling(models.get_sensors_data, username, device_id)


def update_sensors(username, device_id, data):
    return do_with_handling(models.update_sensors_data, username, device_id, data)


def device_create_slot(username):
    slot = models.get_device_slot(username)
    return jsonify({'token': slot['device_id']})


def device_attach(device_id):
    new_id = str(secrets.token_hex(16))
    ex = do_with_handling(models.update_device, device_id,
                          {'device_id': new_id, 'last_online': datetime.datetime.utcnow(), 'name': "GrowECO"})
    if ex[1] == 400:
        return ex
    else:
        return jsonify({'token': new_id})


def get_devices(username, last=False):
    devices = models.get_devices(username)
    if not last:
        return jsonify(list(devices))
    else:
        return jsonify(list(devices)[-1])


def update_device(device_id, data):
    fields = ['name']
    new_data = dict()
    for field in fields:
        if field in data:
            new_data[field] = data[field]
    return do_with_handling(models.update_device, device_id, new_data)


def do_with_handling(f, *args):
    try:
        return jsonify(f(*args)), 200
    except exceptions.ServerErrorException as e:
        return e.get_json(), 400


def add_action(token, data):
    return do_with_handling(models.add_action, token, data)


def get_action(token):
    try:
        action = models.get_action(token)
    except exceptions.ServerErrorException as e:
        return e.get_json(), 400
    return jsonify(action)
