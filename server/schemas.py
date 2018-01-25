
class DBSchemas:

    SENSORS_SCHEMA = {
        'device_id': None,
        'air_humidity': 0,
        'air_temperature': 0,
        'ground_humidity': 0,
        'ground_temperature': 0,
        'pressure': 0,
        'water' : 0
    }

    DEVICE_SCHEMA = {
        'token': None,
        'name': "GrowECO",
        'owner': None,
        'is_attached': False,
        'last_online': None
    }

    ACTIONS_SCHEMA = {
        'device_id': None,
        'actions': []
    }

    @staticmethod
    def create_sensors_schema(device_id):
        record = DBSchemas.SENSORS_SCHEMA.copy()

        record['device_id'] = device_id

        return record

    @staticmethod
    def create_device_schema(owner, token):
        record = DBSchemas.DEVICE_SCHEMA.copy()

        record['owner'] = owner
        record['token'] = token

        return record

    @staticmethod
    def create_actions_schema(device_id):
        record = DBSchemas.ACTIONS_SCHEMA.copy()

        record['device_id'] = device_id

        return record
