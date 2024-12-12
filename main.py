from flask import Flask, request, jsonify, render_template
import mediapipe as mp
import cv2
import numpy as np
import base64
import os
from model.gesture_detector import dedos_levantados, detectar_numero

app = Flask(__name__)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process_frame", methods=["POST"])
def process_frame():
    try:
        data = request.get_json()
        image_data = data.get("image", None)
        if not image_data:
            raise ValueError("No se recibió ninguna imagen.")

        image_bytes = base64.b64decode(image_data.split(",")[1])
        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("No se pudo decodificar la imagen.")

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                dedos = dedos_levantados(hand_landmarks.landmark)
                numero = detectar_numero(dedos, hand_landmarks.landmark)
                return jsonify({"numero": numero, "landmarks": dedos})

        return jsonify({"numero": "No se detectaron manos", "landmarks": []})

    except Exception as e:
        print(f"Error procesando el fotograma: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.template_folder = os.path.join(os.getcwd(), "templates")

    # Cambiar host para permitir conexiones en la red local
    app.run(host="192.168.8.103", port=5000, debug=True)
