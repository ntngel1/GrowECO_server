from flask_httpauth import HTTPBasicAuth
from pymongo import MongoClient
import secrets

import config
from server import app
from server.exceptions import *
from server.schemas import DBSchemas

auth = HTTPBasicAuth()
mongodb = MongoClient(config.DB_URI)
db = mongodb[config.DB_NAME]

@auth.verify_password
def verify_pw(username, password):
    if username == '' or password == '':
        return False

    user = db.users.find_one({'username': username})

    if user:
        if user['password'] == password:
            return True
        else:
            return False


def check_device_owner(username, token):
    user = db.users.find_one({'username': username})
    device = db.devices.find_one({'token': token})
    if device is None:
        raise InvalidDeviceTokenException()

    if device['owner'] == user['_id']:
        return True
    else:
        return False


def check_device_exists(params):
    return db.devices.find(params).count() > 0 if True else False


def create_user(user_data):
    errors = dict()

    if db.users.find({'username': user_data['username']}).count() > 0:
        errors['username'] = "Данный никнейм уже используется!"

    if db.users.find({'email': user_data['email']}).count() > 0:
        errors['email'] = "Данный email уже используется!"

    if errors:
        e = DataNotSuitableException(errors)
        raise e
    db.users.insert(user_data)
    return True


def get_user(username):
    user = db.users.find_one({'username': username})
    return user


def update_user(username, update_data):
    db.users.update({'username': username},
                    {'$set': update_data})
    return True


def get_sensors(token):
    device = db.devices.find_one({'token': token})
    if not device:
        raise InvalidDeviceTokenException()

    sensors = db.sensors.find_one({'device_id': device['_id']})
    if not sensors:
        sensors = DBSchemas.create_sensors_schema(device['_id'])
        db.sensors.insert(sensors)

    return sensors


def update_sensors(token, values):
    device = db.devices.find_one({'token': token})
    if not device:
        raise InvalidDeviceTokenException()

    if db.sensors.find({'device_id': device['_id']}).count() == 0:
        db.sensors.insert(DBSchemas.create_sensors_schema(device['_id']))

    db.sensors.update({'device_id': device['_id']},
                      {'$set': values})
    return True


def create_device(owner, token):
    user = db.users.find_one({'username': owner})
    db.devices.insert({'owner': user['_id'], 'token': token, 'last_online': None})


def get_devices(owner):
    user = db.users.find_one({'username': owner})
    return db.devices.find({'owner': user['_id'], 'is_attached': True})


def get_device_slot(owner):
    user = db.users.find_one({'username': owner})

    device = db.devices.find_one({'owner': user['_id'], 'is_attached': False})
    if device:
        return device

    record = DBSchemas.create_device_schema(user['_id'], str(secrets.token_hex(4)))
    db.devices.insert(record)

    return record


def update_device(token, data):
    if check_device_exists({'token': token}):
        db.devices.update({'token': token}, {'$set': data})
        return data
    else:
        raise InvalidDeviceTokenException()


def create_action(token, data):
    if not check_device_exists({'token': token}):
        raise InvalidDeviceTokenException()

    device = db.devices.find_one({'token': token})
    actions = db.actions.find_one({'device_id': device['_id']})

    if not actions:
        record = DBSchemas.create_actions_schema(device['_id'])
        db.actions.insert(record)

    db.actions.update_one({'device_id': device['_id']}, {'$push': {'actions': data}})
    return True


def get_action(token):
    if check_device_exists({'token': token}):
        device = db.devices.find_one({'token': token})
        actions = db.actions.find_one({'device_id': device['_id']})
        if not actions:
            return None

        action = dict()
        try:
            action["action"] = actions['actions'][0]
        except:
            return None
        db.actions.update_one({'device_id': device['_id']}, {'$pop': {'actions': -1}})
        return action
    else:
        raise InvalidDeviceTokenException()


def get_settings(token):
    if check_device_exists({'token': token}):
        device = db.devices.find_one({'token': token})
        settings = db.settings.find_one({'device_id': device['_id']})
        if not settings:
            settings = DBSchemas.create_settings_schema(device['_id'])
            db.settings.insert(settings)

        db.settings.update_one({'device_id': device['_id']}, {'$set':{'has_updates': False}})

        return settings
    else:
        raise InvalidDeviceTokenException()

def update_settings(token, data):
    if check_device_exists({'token': token}):
        device = db.devices.find_one({'token': token})
        settings = db.settings.find_one({'device_id': device['_id']})
        if not settings:
            settings = DBSchemas.create_settings_schema(device['_id'])
            db.settings.insert(settings)
        data['has_updates'] = True
        db.settings.update_one({'device_id': device['_id']}, {'$set': data})
    else:
        raise InvalidDeviceTokenException()

def has_settings_updates(token):
    if check_device_exists({'token': token}):
        device = db.devices.find_one({'token': token})
        settings = db.settings.find_one({'device_id': device['_id']})
        if not settings:
            settings = DBSchemas.create_settings_schema(device['_id'])
            db.settings.insert(settings)

        return settings['has_updates']
    else:
        raise InvalidDeviceTokenException()
