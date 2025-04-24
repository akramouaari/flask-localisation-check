from flask import Flask, request, jsonify
from flask_cors import CORS
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)
CORS(app)

CENTER_LAT = 35.769662
CENTER_LON = -5.834378
RADIUS_KM = 0.5  # نصف قطر الدائرة 1 كم

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

@app.route("/check-location", methods=["POST"])
def check_location():
    data = request.get_json()
    user_lat = data.get("latitude")
    user_lon = data.get("longitude")
    if user_lat is None or user_lon is None:
        return jsonify({"status": "error", "message": "Missing coordinates"}), 400

    distance = haversine(CENTER_LAT, CENTER_LON, user_lat, user_lon)
    if distance <= RADIUS_KM:
        return jsonify({"status": "ok", "message": "You are allowed"})
    else:
        return jsonify({"status": "denied", "message": "Your area is not supported yet"})

if __name__ == "__main__":
    app.run()
