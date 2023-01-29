from flask import Flask, jsonify, request
from flask_restful import Api
from dotenv import load_dotenv
import src.utils.watchdog as watchdog
import os

from src.services import calculate_room_temperature
import src.utils.es_manager as es_manager

load_dotenv(verbose=True)
app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)

# Elastic search environment parameters to fetch data from elastic search
es_config = {
    'host': os.getenv('ELASTICSEARCH_HOST'),
    'port': int(os.getenv('ELASTICSEARCH_PORT')),
    'username': os.getenv('ELASTICSEARCH_USERNAME'),
    'password': os.getenv('ELASTICSEARCH_PASSWORD'),
}
es_man = es_manager.ESConnection(**es_config)


@app.route("/calculate-room-temperature", methods=["GET"])
def get_room_temperature():
    return calculate_room_temperature(es_man, request.args)


@app.errorhandler(404)
def not_found(_error=None):
    message = {
        "status": 404,
        "message": "Not Found: " + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    watchdog.logger.info("Starting app")
    app.run(host="0.0.0.0", port=8000, debug=True)
