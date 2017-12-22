import base64

from flask_httpauth import HTTPBasicAuth
from pymongo import MongoClient
import datetime
import secrets

import config
from server import exceptions

auth = HTTPBasicAuth()
db_client = MongoClient(config.DB_HOST, config.DB_PORT)
db = db_client.GrowECO


@auth.verify_password
def verify_pw(username, password):
    if username == '' or password == '':
        return False

    if db.users.find_one({'username': username}):
        if db.users.find_one({'username': username})['password'] == password:
            return True
        else:
            return False
    else:
        return False


def create_user(user_data):
    errors = dict()

    if db.users.find({'username': user_data['username']}).count() > 0:
        errors['username'] = "Данный никнейм уже используется!"

    if db.users.find({'email': user_data['email']}).count() > 0:
        errors['email'] = "Данный email уже используется!"

    if errors:
        raise exceptions.ServerErrorException(exceptions.ErrorCode.DATA_NOT_SUITABLE, errors, "Неверные данные!")
    else:
        db.users.insert(user_data)
        return True


def get_user(username):
    user = db.users.find_one({'username': username}, {'_id': 0, 'password': 0})
    return user


def update_user(username, update_data):
    db.users.update({'username': username},
                    {'$set': update_data})
    return True


def check_device_owner(username, device_id):
    user = db.users.find_one({'username': username})
    device = db.devices.find_one({'device_id': device_id})
    if device is None:
        raise exceptions.ServerErrorException(exceptions.ErrorCode.DEVICE_NOT_REGISTERED,
                                              message="Данное устройство не зарегистрировано!")
    if device['owner'] == user['_id']:
        return True
    else:
        raise exceptions.ServerErrorException(exceptions.ErrorCode.NOT_OWNER,
                                              message="Вы не являетесь владельцем данного устройства!")


def get_sensors_data(username, device_id):
    if check_device_owner(username, device_id):
        device = db.devices.find_one({'device_id': device_id})
        sensors = db.sensors.find_one({'device_id': device['_id']}, {'_id': 0, 'device_id': 0})
        return sensors


def update_sensors_data(username, device_id, data):
    if check_device_owner(username, device_id):
        fields = ['air_humidity', 'air_temperature', 'ground_humidity', 'ground_temperature']
        new_data = dict()
        for field in fields:
            if field in data:
                new_data[field] = data[field]
            else:
                new_data[field] = 0
        device = db.devices.find_one({'device_id': device_id})

        if db.sensors.find({'device_id': device['_id']}).count() == 0:
            db.sensors.insert({'device_id': device['_id']})
        db.sensors.update({'device_id': device['_id']},
                          {'$set': new_data})
        return True


def create_device(owner, device_id):
    user = db.users.find_one({'username': owner})
    db.devices.insert({'owner': user['_id'], 'device_id': device_id, 'last_online': None})


def get_devices(owner):
    user = db.users.find_one({'username': owner})
    return db.devices.find({'owner': user['_id'], 'last_online': {'$ne': None}}, {'_id': 0, 'owner': 0})


def check_device_exists(params):
    return db.devices.find(params).count() > 0 if True else False


def get_device_slot(owner):
    user = db.users.find_one({'username': owner})
    device = db.devices.find_one({'owner': user['_id'], 'last_online': None})
    if device:
        return device
    else:
        create_device(owner, str(secrets.token_hex(4)))
        return db.devices.find_one({'owner': user['_id'], 'last_online': None})


def update_device(device_id, data):
    if check_device_exists({'device_id': device_id}):
        db.devices.update({'device_id': device_id}, {'$set': data})
        return True
    else:
        raise exceptions.ServerErrorException(exceptions.ErrorCode.INVALID_DEVICE_TOKEN,
                                              message="Недействительный токен устройства!")


def add_action(token, data):
    if check_device_exists({'device_id': token}):
        actions = db.actions.find_one({'device_id': token})
        if not actions:
            actions = db.actions.insert_one({'device_id': token, 'actions': []})

        db.actions.update_one({'device_id': token}, {'$push': {'actions': data}})
        return True
    else:
        raise exceptions.ServerErrorException(exceptions.ErrorCode.INVALID_DEVICE_TOKEN,
                                              message="Недействительный токен устройства!")


def get_action(token):
    if check_device_exists({'device_id':token}):
        actions = db.actions.find_one({'device_id': token})
        if not actions or len(actions['actions']) == 0:
            return None

        action = dict(actions['actions'][0])
        db.actions.update_one({'device_id':token}, {'$pop': {'actions': -1}})
        return action
    else:
        raise exceptions.ServerErrorException(exceptions.ErrorCode.INVALID_DEVICE_TOKEN,
                                              message="Недействительный токен устройства!")
