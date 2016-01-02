from flask import Flask
from flask import jsonify
import services

app = Flask(__name__)

@app.route("/")
def index():
    services.turn_on_living_room()

    return jsonify({
        "response": "on"
    })

@app.route("/on")
def living_room_on():
    services.turn_on_living_room()

    return jsonify({
        "response": "on"
    })

@app.route("/off")
def living_room_off():
    services.turn_off_living_room()

    return jsonify({
        "response": "off"
    })
