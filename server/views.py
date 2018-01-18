from flask import request

from server import app
from server import controllers
from server import models


@app.route('/user/create', methods=['POST'])
def create_user():
    return controllers.create_user(request.get_json())


@app.route('/user/get')
@models.auth.login_required
def get_user():
    return controllers.get_user(models.auth.username())


@app.route('/user/update', methods=['PUT'])
@models.auth.login_required
def update_user():
    return controllers.update_user(models.auth.username(), request.get_json())


@app.route('/sensors/get/<token>')
def get_sensors(token):
    return controllers.get_sensors(token)


@app.route('/sensors/update/<token>', methods=['PUT'])
def update_sensors(token):
    return controllers.update_sensors(token, request.get_json())


@app.route('/device/create_slot')
@models.auth.login_required
def get_device_slot():
    return controllers.get_device_slot(models.auth.username())


@app.route('/device/attach/<token>')
def attach_device(token):
    return controllers.attach_device(token)


@app.route('/device/get_devices')
@models.auth.login_required
def get_devices():
    return controllers.get_devices(models.auth.username())


@app.route('/device/update/<token>', methods=['PUT'])
def update_device(token):
    return controllers.update_device(token, request.get_json())


@app.route('/device/get_last')
@models.auth.login_required
def get_last_device():
    return controllers.get_devices(models.auth.username(), last=True)


@app.route('/actions/create/<token>', methods=['POST'])
def create_action(token):
    return controllers.create_action(token, request.get_json())


@app.route('/actions/get/<token>')
def get_action(token):
    return controllers.get_action(token)

