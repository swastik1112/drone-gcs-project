from flask import Flask, jsonify, request
from flask_cors import CORS 
from pymavlink import mavutil
import threading
import time

app = Flask(__name__)
CORS(app) 

telemetry_data = {
    "gps": {"lat": 40.7128, "lon": -74.0060},
    "altitude": {"meters": 120},
    "battery": {"voltage": 95}
}

def meters_to_feet(meters):
    return meters * 3.28084

def mavlink_listener():
    try:
        print("Starting MAVLink listener...")
    
        connection = mavutil.mavlink_connection('udp:localhost:14550')
        connection.wait_heartbeat(timeout=10) 
        print("MAVLink connection established")

        connection.mav.request_data_stream_send(
            connection.target_system,
            connection.target_component,
            mavutil.mavlink.MAV_DATA_STREAM_ALL,
            1, 1
        )

        while True:
            message = connection.recv_match(blocking=True, timeout=5)

            if message:
                message_type = message.get_type()

                if message_type == 'GPS_RAW_INT':
 
                    telemetry_data['gps'] = {
                        'lat': message.lat / 1e7,
                        'lon': message.lon / 1e7
                    }
                    print(f"Updated GPS data: {telemetry_data['gps']}")

                elif message_type == 'BATTERY_STATUS':
               
                    telemetry_data['battery'] = {
                        'voltage': message.voltages[0] / 1000  
                    }
                    print(f"Updated battery data: {telemetry_data['battery']}")

                elif message_type == 'GLOBAL_POSITION_INT':
                    
                    altitude_meters = message.alt / 1000 
                    telemetry_data['altitude'] = {
                        'meters': altitude_meters,
                        'feet': meters_to_feet(altitude_meters)
                    }
                    print(f"Updated altitude data: {telemetry_data['altitude']}")

                time.sleep(1)  
    except Exception as e:
        print(f"Error in MAVLink listener: {e}")


@app.route('/telemetry', methods=['GET'])
def get_telemetry():
    try:
        print("Fetching telemetry data: ", telemetry_data)
        return jsonify(telemetry_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update-altitude', methods=['POST'])
def update_altitude():
    try:
        data = request.get_json()
        altitude = data.get('altitude')

        if altitude is not None:
            telemetry_data['altitude'] = {
                'meters': float(altitude),
                'feet': meters_to_feet(float(altitude))
            }
            return jsonify({
                "message": "Altitude updated successfully",
                "data": telemetry_data
            }), 200
        else:
            return jsonify({"error": "Altitude value is required"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_flask():
    app.run(debug=True, host='127.0.0.1', port=5000)

if __name__ == "__main__":

    mavlink_thread = threading.Thread(target=mavlink_listener)
    mavlink_thread.daemon = True
    mavlink_thread.start()

    run_flask()
