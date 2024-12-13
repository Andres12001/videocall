from flask import Flask, request, jsonify, render_template
import mediapipe as mp
import cv2
import numpy as np
import base64
import os
from model.numeros import dedos_levantados, detectar_numero  # Importar desde numeros.py
from model.saludos import detectar_palabra  # Importar desde saludos.py
from model.acciones import detectar_accion  # Importar desde acciones.py

app = Flask(__name__)

# Variable global para el subtítulo compartido
global_subtitulo = {"texto": ""}
modo_reconocimiento = "gesto"  # Modo por defecto

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/set_mode", methods=["POST"])
def set_mode():
    global modo_reconocimiento
    data = request.get_json()
    modo = data.get("modo", "gesto")
    
    if modo in ["numero", "saludo", "accion"]:  # Validar los modos permitidos
        modo_reconocimiento = modo
        return jsonify({"status": "ok", "modo": modo_reconocimiento})
    else:
        return jsonify({"status": "error", "message": "Modo desconocido"}), 400

@app.route("/process_frame", methods=["POST"])
def process_frame():
    global global_subtitulo
    try:
        data = request.get_json()
        image_data = data.get("image", None)
        if not image_data:
            raise ValueError("No se recibió ninguna imagen.")

        # Decodificar la imagen Base64
        image_bytes = base64.b64decode(image_data.split(",")[1])
        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("No se pudo decodificar la imagen.")

        # Convertir la imagen a RGB para MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                dedos = dedos_levantados(hand_landmarks.landmark)

                if modo_reconocimiento == "numero":
                    resultado = detectar_numero(dedos, hand_landmarks.landmark)
                elif modo_reconocimiento == "saludo":
                    resultado = detectar_palabra(dedos, hand_landmarks.landmark)
                elif modo_reconocimiento == "accion":
                    resultado = detectar_accion(dedos, hand_landmarks.landmark)
                else:
                    resultado = "Modo desconocido"

                global_subtitulo["texto"] = resultado
                return jsonify({"resultado": resultado})

        global_subtitulo["texto"] = "No se detectaron manos"
        return jsonify({"resultado": "No se detectaron manos"})

    except Exception as e:
        print(f"Error procesando el fotograma: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/get_subtitle", methods=["GET"])
def get_subtitle():
    global global_subtitulo
    return jsonify(global_subtitulo)

if __name__ == "__main__":
    app.template_folder = os.path.join(os.getcwd(), "templates")
    app.run(host="127.0.0.1", port=5000, debug=True)
