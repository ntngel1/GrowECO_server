from flask import request
from flask import jsonify

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

@app.route('/sensors/get/<id>')
@models.auth.login_required
def get_sensors(id):
    return controllers.get_sensors(models.auth.username(), id)

@app.route('/sensors/update/<id>', methods=['PUT'])
@models.auth.login_required
def update_sensors(id):
    return controllers.update_sensors(models.auth.username(), id, request.get_json())