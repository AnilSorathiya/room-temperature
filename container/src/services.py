import os
import joblib
from flask import jsonify
from dotenv import load_dotenv
from .utils import watchdog as watchdog
from .middleware import validate_request
from .enums import APIParams, ModelColumns, ESColumns
import json
from numpyencoder import NumpyEncoder

# used to retrieve last X minutes data from database
MINUTES = -30
hub2_hw_revisions = ["2A", "2E"]
INDEX = os.getenv('ELASTICSEARCH_INDEX_DEVICE_SUMMARY')
load_dotenv(verbose=True)

# Model has been used for hardware revision 1
ml_scaler = joblib.load(open('./src/models/scaler.sav', 'rb'))

# Model has been used for hardware revision 1
model = joblib.load(open('./src/models/lin_model_hardware_2A.sav', 'rb'))
# Model has been used for hardware revision 2
model_2E = joblib.load(open('./src/models/lin_model_hardware_2E.sav', 'rb'))


def calculate_room_temperature(es_man, *args):
    data, errors = validate_request(args)
    watchdog.logger.info(data)
    if len(errors) > 0:
        return arg_error(errors=errors)

    room_temperature = data[APIParams.ROOM_TEMPERATURE.value]
    light_brightness = data[APIParams.LIGHT_BRIGHTNESS.value]
    processor_temperature = data[APIParams.PROCESSOR_TEMPERATURE.value]
    hub_hw_revision = data[APIParams.HUB_HW_REVISION.value]

    # retrieve data
    try:
        # In this prototype we are not connecting to database
        # query = build_query(start_at, MINUTES, family_device_id)
        # result = es_man.request_data(index=INDEX, query=query)
        # data = result["aggregations"]["avgValues"]
        data = []
        watchdog.logger.info(data)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        return error_message("device", ex, room_temperature, template)

    d_room_temperature = room_temperature
    d_light_brightness = light_brightness
    d_processor_temperature = processor_temperature

    # compute new features
    if len(data) != 0:
        d_room_temperature = data[ModelColumns.AVG_ROOM_TEMPERATURE.value]['value']
        d_light_brightness = data[ModelColumns.AVG_LIGHT_BRIGHTNESS.value]['value']
        d_processor_temperature = data[ModelColumns.AVG_PROCESSOR_TEMPERATURE.value]['value']

    if (d_room_temperature is None) | (d_light_brightness is None) | (d_processor_temperature is None):
        d_room_temperature = room_temperature
        d_light_brightness = light_brightness
        d_processor_temperature = processor_temperature
        watchdog.logger.info("Database is returning None")

        watchdog.logger.info([d_room_temperature, d_light_brightness, d_processor_temperature])

    try:
        watchdog.logger.info(model)
        watchdog.logger.info([d_room_temperature, d_light_brightness, d_processor_temperature])
        watchdog.logger.info("Predict room temperature using Linear regression model")

        if hub_hw_revision == '1B':
            x_test_scaled = ml_scaler.transform([[d_room_temperature, d_light_brightness, d_processor_temperature]])
            watchdog.logger.info(x_test_scaled)
            predicted_room_temperature = model.predict(x_test_scaled) - 1.0
        elif hub_hw_revision in hub2_hw_revisions:
            predicted_room_temperature = model_2E.predict(
                [[d_room_temperature, d_light_brightness, d_processor_temperature]])
            watchdog.logger.info(predicted_room_temperature)

    except Exception as ex:
        template = "Something went wrong while computing room temperature.\n" \
                   "An exception of type {0} occurred. Arguments:\n{1!r}"
        return error_message("device", ex, room_temperature, template)

    result = {
        "originalRoomTemperature": room_temperature,
        APIParams.ROOM_TEMPERATURE.value: predicted_room_temperature.tolist()[0],
    }

    watchdog.logger.info("result", result)
    result = json.dumps(result, cls=NumpyEncoder, indent=4)
    return result, 200


# This function has not been used as we are not connecting to elastic search yet
def build_query(current_start_at, minutes, device_id):
    """
    build query to retrieve average of light brightness, room temperature and processor temperature
     of given device id of last x minutes
    :param current_start_at: given current time
    :param minutes: number of minutes to retrieve pass data
    :param device_id: hub -  device id
    :return: query string
    """
    back_start_at = current_start_at + (60 * minutes)
    query = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {"match": {ESColumns.FAMILY_DEVICE_ID.value: device_id}},
                    {"match": {ESColumns.DEVICE_TYPE.value: "hub"}}
                ]
            }
        },
        "aggs": {
            "avgValues": {
                "filter": {"range": {ESColumns.START_AT.value:
                                         {"gte": back_start_at, "lte": current_start_at}}},
                "aggs": {
                    ModelColumns.AVG_LIGHT_BRIGHTNESS.value: {
                        "avg": {"field": ESColumns.LIGHT_BRIGHTNESS.value}},
                    ModelColumns.AVG_ROOM_TEMPERATURE.value: {
                        "avg": {"field": ESColumns.ROOM_TEMPERATURE.value}},
                    ModelColumns.AVG_PROCESSOR_TEMPERATURE.value: {
                        "avg": {"field": ESColumns.PROCESSOR_TEMPERATURE.value}}
                }
            }
        }
    }
    watchdog.logger.info(query)
    return query


def error_message(device_id, ex, room_temperature, template):
    return jsonify({
        "message": template.format(type(ex).__name__, ex.args),
        "error": str(ex),
        APIParams.FAMILY_DEVICE_ID.value: device_id,
        "originalTemp": room_temperature,
    }), 500


def arg_error(errors):
    return json.dumps({'error': errors}), 400
