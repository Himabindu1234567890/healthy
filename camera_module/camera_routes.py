from flask import Blueprint, render_template, request, jsonify
import base64
import cv2
import numpy as np

camera_bp = Blueprint("camera", __name__)

@camera_bp.route("/camera")
def camera_page():
    return render_template("camera.html")

@camera_bp.route("/capture", methods=["POST"])
def capture():
    try:
        data = request.json

        image_data = data["image"].split(",")[1]
        image_bytes = base64.b64decode(image_data)
        np_img = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({"error": "Invalid image"}), 400

        items = data.get("items", [])
        results = []
        total_weight = 0

        MEASURE_GRAMS = {
            "piece": 100, "cup": 240, "bowl": 300,
            "spoon": 15, "plate": 350, "glass": 250
        }

        SIZE_MULTIPLIER = {
            "small": 0.75, "medium": 1.0, "large": 1.25
        }

        for item in items:
            measure = item.get("measure", "piece")
            size = item.get("size", "medium")
            count = int(item.get("count", 1))

            base = MEASURE_GRAMS.get(measure, 100)
            factor = SIZE_MULTIPLIER.get(size, 1.0)

            weight = base * factor * count
            total_weight += weight

            results.append({
                "name": item.get("name", "unknown"),
                "weight_grams": round(weight, 2)
            })

        return jsonify({
            "items": results,
            "total_weight_grams": round(total_weight, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
