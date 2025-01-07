import os
import logging
import face_recognition
import cv2
import numpy as np
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

STORED_PHOTOS_DIR = "images"

def load_stored_photos():
    stored_encodings = []
    photo_names = []
    logging.info("Loading stored photos...")

    for file_name in os.listdir(STORED_PHOTOS_DIR):
        if file_name.lower().endswith(('jpg', 'jpeg', 'png')):
            file_path = os.path.join(STORED_PHOTOS_DIR, file_name)
            logging.info(f"Processing {file_name}...")

            image = face_recognition.load_image_file(file_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                stored_encodings.extend(encodings)
                photo_names.extend([file_name] * len(encodings))
                logging.info(f"Found {len(encodings)} face(s) in {file_name}.")
            else:
                logging.warning(f"No face found in {file_name}. Skipping.")

    return stored_encodings, photo_names

stored_encodings, photo_names = load_stored_photos()

def compare_photo(new_image):
    face_locations = face_recognition.face_locations(new_image)
    if not face_locations:
        return None, "No face detected."

    new_encodings = face_recognition.face_encodings(new_image, face_locations)
    for new_encoding in new_encodings:
        results = face_recognition.compare_faces(stored_encodings, new_encoding, tolerance=0.5)
        if True in results:
            match_index = results.index(True)
            return photo_names[match_index], "Match found."

    return None, "No match found."

@app.route('/compare', methods=['POST'])
def compare():
    if 'photo' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['photo']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Optimize image loading and resizing
        image = face_recognition.load_image_file(file)
        small_image = cv2.resize(image, (256, 256))  # Resize for faster processing

        matched_photo, message = compare_photo(small_image)

        if matched_photo:
            return jsonify({"matched_photo": matched_photo, "message": message}), 200
        else:
            return jsonify({"message": message}), 200
    except Exception as e:
        logging.error(f"Error comparing photo: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
