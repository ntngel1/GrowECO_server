from server.exceptions import *

class RequestDataPreprocessor:

    @staticmethod
    def create_user_data(json):
        user_fields = ['name', 'username', 'password', 'email']

        errors = dict()
        data = dict()

        for field in user_fields:
            if field in json:
                data[field] = json[field]
            else:
                errors[field] = ["Обязательное параметр!"]

        if errors:
            e = DataNotSuitableException(errors, "Отсутствуют некоторые параметры!")
            raise e

        return data

    @staticmethod
    def update_user_data(json):
        user_fields = ['name', 'email']

        data = dict()

        for field in user_fields:
            if field in json:
                data[field] = json[field]

        return data

    @staticmethod
    def update_sensors_data(json):
        sensors_fields = ['air_humidity', 'air_temperature', 'ground_humidity', 'ground_temperature', 'water']

        data = dict()

        for field in sensors_fields:
            if field in json:
                data[field] = json[field]

        return data

    @staticmethod
    def update_device_data(json):
        device_fields = ['name']

        data = dict()

        for field in device_fields:
            if field in json:
                data[field] = json[field]

        return data

    @staticmethod
    def create_action(json):
        action_fields = ['action_code']

        data = dict()

        for field in action_fields:
            if field in json:
                data[field] = json[field]

        return data


class ResponseDataPreprocessor:

    @staticmethod
    def get_user_data(data):
        user_fields = ['name', 'username', 'email']

        json = dict()

        for field in user_fields:
            json[field] = data[field]

        return json

    @staticmethod
    def get_sensors_data(data):
        sensors_fields = ['air_humidity', 'air_temperature', 'ground_humidity', 'ground_temperature', 'water']

        json = dict()

        for field in sensors_fields:
            json[field] = data[field]

        return json

    @staticmethod
    def get_device_slot(data):
        json = dict()
        json['token'] = data['token']

        return json

    @staticmethod
    def attach_device(data):
        json = dict()
        json['token'] = data['token']

        return json

    @staticmethod
    def get_device(data):
        device_fields = ['token', 'name', 'last_online']

        json = dict()

        for field in device_fields:
            json[field] = data[field]

        return json
