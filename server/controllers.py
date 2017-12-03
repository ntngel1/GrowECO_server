from flask import jsonify
from server import models
from server import exceptions


def register_account(req_data):
    params = ['name', 'username', 'password', 'email']
    newUserData = {}

    errors = {}
    hasErrors = False

    if req_data is None:
        return jsonify("Registration data is missing")

    for param in params:
        try:
            newUserData[param] = req_data[param]
        except KeyError:
            errors[param] = "Parameter %s can't be null" % param
            hasErrors = True

    if not hasErrors:
        return jsonify(models.create_user(newUserData))
    else:
        return jsonify(errors)


def get_account(username):
    return jsonify(models.get_user(username))


def update_account(username, req_data):
    params = ['name', 'username', 'password', 'email']
    new_user_data = {}

    if req_data is None:
        return jsonify("Update data is missing")

    for param in params:
        try:
            new_user_data[param] = req_data[param]
        except KeyError:
            continue

    return jsonify(models.update_user(username, new_user_data))


def get_sensors(username, id):
    try:
        data = models.get_sensors_data(username, id)
    except Exception as ex:
        return jsonify(str(ex)), 400

    return jsonify(data)


def update_sensors(username, id, data):
    try:
        return jsonify(models.update_sensors_data(username, id, data))
    except Exception as ex:
        return jsonify(str(ex)), 400
