from flask import request

from server import app
from server import controllers
from server import models


@app.route('/account/register', methods=['POST'])
def register_account():
    return controllers.register_account(request.get_json())


@app.route('/account/get')
@models.auth.login_required
def get_account():
    return controllers.get_account(models.auth.username())


@app.route('/account/update', methods=['PUT'])
@models.auth.login_required
def update_account():
    return controllers.update_account(models.auth.username(), request.get_json())


@app.route('/sensors/get/<device_id>')
@models.auth.login_required
def get_sensors(device_id):
    return controllers.get_sensors(models.auth.username(), device_id)


@app.route('/sensors/update/<device_id>', methods=['PUT'])
@models.auth.login_required
def update_sensors(device_id):
    return controllers.update_sensors(models.auth.username(), device_id, request.get_json())


@app.route('/device/create_slot')
@models.auth.login_required
def device_create_slot():
    return controllers.device_create_slot(models.auth.username())


@app.route('/device/attach/<device_id>')
def device_attach(device_id):
    return controllers.device_attach(device_id)