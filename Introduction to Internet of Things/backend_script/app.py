from flask import Flask, jsonify, request
from flask_cors import CORS
import paho.mqtt.client as mqtt
import logging
from datetime import datetime
import base64
import os

app = Flask(__name__)
CORS(app)

# Ensure a directory for saving images exists
os.makedirs("captured_images", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Set up logging for sprinkler status and detection results
logging.basicConfig(filename=os.path.join("logs", "general_logs.log"), level=logging.INFO, format='%(asctime)s - %(message)s')

# Loggers for each topic
loggers = {
    "sprinkler_status": logging.getLogger("sprinkler_status"),
    "danger": logging.getLogger("danger_status"),
    "temperature": logging.getLogger("temperature"),
    "gas_level": logging.getLogger("gas_level"),
    "captured_image": logging.getLogger("captured_image")
}

# File handlers for each logger
loggers["sprinkler_status"].addHandler(logging.FileHandler(os.path.join("logs", "sprinkler_status.log")))
loggers["danger"].addHandler(logging.FileHandler(os.path.join("logs", "danger_status.log")))
loggers["temperature"].addHandler(logging.FileHandler(os.path.join("logs", "temperature.log")))
loggers["gas_level"].addHandler(logging.FileHandler(os.path.join("logs", "gas_level.log")))
loggers["captured_image"].addHandler(logging.FileHandler(os.path.join("logs", "captured_image.log")))


# MQTT setup
MQTT_BROKER = "IP_ADDRESS"  # IP of laptop

MQTT_PORT = 1883
SPRINKLER_ACTION_TOPIC = "pyroshield/sprinkler_action"  # ON or OFF (Sent to ESP32)
SPRINKLER_STATUS_TOPIC = "pyroshield/sprinkler_status"  # Sprinkler activated or Sprinkler deactivated (Sent by ESP32)
DETECTION_RESULT_TOPIC = "pyroshield/danger"            # Safety status danger state
THERMOCAM_TEMP_TOPIC = "pyroshield/temp"                # Thermocamera reading
GAS_SENSOR_VAL_TOPIC = "pyroshield/gasLevel"            # Gas sensor reading
CAPTURED_IMAGE_TOPIC = "pyroshield/cam_image"           # Image captured from camera

# Status storage
gasCheck = False
safetyCheck = False
sprinkler_status = {"status": "OFF"}
sprinkler_message_history = []
safety_status = {"danger": "Unknown", "temperature": None, "gasLevel": None}


# Define MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code", rc)
    client.subscribe(SPRINKLER_STATUS_TOPIC)
    client.subscribe(DETECTION_RESULT_TOPIC)    
    client.subscribe(THERMOCAM_TEMP_TOPIC)    
    client.subscribe(GAS_SENSOR_VAL_TOPIC)
    client.subscribe(CAPTURED_IMAGE_TOPIC)

def on_message(client, userdata, msg):
    global sprinkler_status, safety_status, gasCheck, safetyCheck

    payload = msg.payload.decode()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if msg.topic == SPRINKLER_STATUS_TOPIC:
        if "deactivated" in payload:
            sprinkler_status["status"] = "OFF"
            message = f"{timestamp}: {payload}"
        elif "activated" in payload:
            sprinkler_status["status"] = "ON"
            message = f"{timestamp}: {payload}, temperature: {safety_status['temperature']}, gas level: {safety_status['gasLevel']}"
        print(f"Updated sprinkler status to: {sprinkler_status['status']}")  # Debugging

        # Keep only the last 10 messages
        if len(sprinkler_message_history) > 10:
            sprinkler_message_history.pop(0)

        # Update status and history
        sprinkler_message_history.append(message)
    
        # Log the message to the file
        loggers["sprinkler_status"].info(message)

    elif msg.topic == DETECTION_RESULT_TOPIC:
        # Overwritting when gasLevel exceed threshold
        gasCheck = safety_status["gasLevel"] is not None and safety_status["gasLevel"] >= 30

        print("Safety status:", safety_status["danger"], "payload:",payload)

        safetyCheck = (payload == "True")

        prevState = safety_status["danger"]
        newState = str(safetyCheck or gasCheck)
    
        # Log the safety status (danger)
        print("prev:",prevState,"new:",newState)
        if (newState != prevState):
            print("change new state")
            safety_status["danger"] = newState
            loggers["danger"].info(f"{timestamp} - {newState}")
            if (newState == "False"):
                safety_status["temperature"] = None
                print("Changed temperature back to",safety_status["temperature"])

            action = "ON" if (newState == "True") else "OFF"
            print("New State?",newState,"Sprinkler current status:",sprinkler_status,"Action to be taken:",action)
            if (sprinkler_status != action):
                print(f"Turning {action}")
                mqtt_client.publish(SPRINKLER_ACTION_TOPIC, action)

    elif msg.topic == THERMOCAM_TEMP_TOPIC:
        # Log the temperature reading (only when status is dangerous)
        safety_status["temperature"] = float(payload) if payload != "null" else None
        loggers["temperature"].info(f"{timestamp} - {payload}")
        
    elif msg.topic == GAS_SENSOR_VAL_TOPIC:
        # Log the gas level with timestamp
        safety_status["gasLevel"] = float(payload)
        loggers["gas_level"].info(f"{timestamp} - {payload}")

    elif msg.topic == CAPTURED_IMAGE_TOPIC:
        image_data = base64.b64decode(payload)
        image_filename = f"captured_images/image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        
        with open(image_filename, "wb") as image_file:
            image_file.write(image_data)
        
        # Log image capture event
        loggers["captured_image"].info(f"{timestamp} - Image saved as {image_filename}")
        print(f"Image saved as {image_filename}")  # Debugging

# Set up MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

# API routes
@app.route("/api/status", methods=["GET"])
def get_status():
    return jsonify(sprinkler_status)

@app.route("/api/activate", methods=["POST"])
def activate_sprinkler():
    action = request.json.get("action")
    if action in ["ON", "OFF"]:
        mqtt_client.publish(SPRINKLER_ACTION_TOPIC, action)
        return jsonify({"message": f"Sprinkler turned {action}"}), 200
    return jsonify({"error": "Invalid action"}), 400

@app.route("/api/messages", methods=["GET"])
def get_messages():
    return jsonify(sprinkler_message_history)

@app.route("/api/detection", methods=["GET"])
def get_ML_result():
    return jsonify(safety_status)

@app.route("/api/gas_history", methods=["GET"])
def get_gas_history():
    gas_data = []
    
    with open("./logs/gas_level.log", "r") as file:
        for line in file:
            timestamp, value = line.strip().split(" - ")
            gas_data.append({"timestamp": timestamp, "value": int(value)})
    
    return jsonify(gas_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
