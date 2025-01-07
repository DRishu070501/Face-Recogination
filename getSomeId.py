import os
import logging
import face_recognition
import cv2
import numpy as np
import base64
import json
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


def load_base64_from_file(file_path):
    with open(file_path, 'r') as f:
        base64_data = json.load(f)  # Assuming the file contains a JSON array of base64 strings
    return base64_data

def decode_base64_image(base64_str):
    """Decodes a Base64 string into a numpy image array"""
    base64_str = base64_str.split(",")[-1]  # Remove the 'data:image' header if present
    image_data = base64.b64decode(base64_str)
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image

def load_stored_photos_from_base64(file_path):
    stored_encodings = []
    photo_names = []
    # logging.info("Loading Base64 encoded images from file...")

    base64_images = load_base64_from_file(file_path)

    for idx, base64_str in enumerate(base64_images):
        if idx == 36:
            print(base64_str)
        # image = decode_base64_image(base64_str)

        # # encodings = face_recognition.face_encodings(image)
        # if encodings:
        #     stored_encodings.extend(encodings)
        #     photo_names.extend([f"Image_{idx}"] * len(encodings))
        #     logging.info(f"Found {len(encodings)} face(s) in Image_{idx}.")
        # else:
        #     logging.warning(f"No face found in Image_{idx}. Skipping.")

    return stored_encodings, photo_names

# Path to the file that contains Base64 encoded images
BASE64_FILE_PATH = "output.txt"

# Load stored images from Base64 file
stored_encodings, photo_names = load_stored_photos_from_base64(BASE64_FILE_PATH)

# def compare_photo(new_image):
#     face_locations = face_recognition.face_locations(new_image)
#     if not face_locations:
#         return None, "No face detected."

#     new_encodings = face_recognition.face_encodings(new_image, face_locations)
#     for new_encoding in new_encodings:
#         results = face_recognition.compare_faces(stored_encodings, new_encoding, tolerance=0.5)
#         if True in results:
#             match_index = results.index(True)
#             return photo_names[match_index], "Match found."

#     return None, "No match found."

# @app.route('/compare', methods=['POST'])
# def compare():
#     if 'photo' not in request.files:
#         return jsonify({"error": "No file part"}), 400

#     file = request.files['photo']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     try:
#         # Optimize image loading and resizing
#         image = face_recognition.load_image_file(file)
#         small_image = cv2.resize(image, (256, 256))  # Resize for faster processing

#         matched_photo, message = compare_photo(small_image)

#         if matched_photo:
#             return jsonify({"matched_photo": matched_photo, "message": message}), 200
#         else:
#             return jsonify({"message": message}), 200
#     except Exception as e:
#         logging.error(f"Error comparing photo: {str(e)}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
