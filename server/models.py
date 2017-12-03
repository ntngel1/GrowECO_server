from flask import jsonify
from flask_httpauth import HTTPBasicAuth
from pymongo import MongoClient

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

def create_user(userData):
    hasErrors = False
    errors = {}

    if db.users.find({'username': userData['username']}).count() > 0:
        errors['username'] = "Username is already in use"
        hasErrors = True

    if db.users.find({'email': userData['email']}).count() > 0:
        errors['email'] = "Email is already in use!"
        hasErrors = True

    if hasErrors:
        return errors
    else:
        db.users.insert(userData)
        return True

def get_user(username):
    user = db.users.find_one({'username': username}, {'_id':0, 'password': 0})
    return user

def update_user(username, update_data):
    db.users.update({'username': username},
                    {'$set': update_data})
    return True

def check_device_permissions(username, device_id):
    user = db.users.find_one({'username': username})
    device = db.devices.find_one({'device_id': int(device_id)})
    if device is None:
        raise exceptions.DeviceException('Device with this id doesn\'t exist! Please register the device')
    if device['owner'] == user['_id']:
        return True
    else:
        raise exceptions.OwnerException('You are not owner of this device')

def get_sensors_data(username, id):
    if check_device_permissions(username, id):
        device = db.devices.find_one({'device_id': int(id)})
        sensors = db.sensors.find_one({'device_id': device['_id']}, {'_id': 0, 'device_id': 0})
        return sensors

def update_sensors_data(username, id, data):
    if check_device_permissions(username, id):
        fields = ['air_humidity', 'air_temperature', 'ground_humidity', 'ground_temperature']
        new_data = dict()
        for field in fields:
            try:
                new_data[field] = data[field]
            except KeyError:
                new_data[field] = 0
        device = db.devices.find_one({'device_id': int(id)})
        db.sensors.update({'device_id': device['_id']},
                          {'$set': new_data})
        return True