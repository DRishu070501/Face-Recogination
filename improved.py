import os
import logging
from flask import Flask, request, jsonify
import face_recognition

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

STORED_PHOTOS_DIR = "images"

def load_stored_photos():
    """
    Loads all stored photos from the directory, encodes faces,
    and returns a list of encodings and corresponding photo names.
    """
    stored_encodings = []
    photo_names = []

    logging.info("Loading stored photos...")

    for file_name in os.listdir(STORED_PHOTOS_DIR):
        if file_name.lower().endswith(('jpg', 'jpeg', 'png')):
            file_path = os.path.join(STORED_PHOTOS_DIR, file_name)
            logging.info(f"Processing {file_name}...")

            image = face_recognition.load_image_file(file_path)
            try:
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    stored_encodings.extend(encodings)
                    photo_names.extend([file_name] * len(encodings))
                    logging.info(f"Found {len(encodings)} face(s) in {file_name}.")
                else:
                    logging.warning(f"No face found in {file_name}. Skipping.")
            except Exception as e:
                logging.error(f"Error processing {file_name}: {str(e)}")

    return stored_encodings, photo_names

stored_encodings, photo_names = load_stored_photos()

def compare_photo(new_image):
    """
    Compares the new image with stored images to find a matching face.
    """
    new_encodings = face_recognition.face_encodings(new_image)
    if not new_encodings:
        return None, "No face detected in the new photo."

    for new_encoding in new_encodings:
        results = face_recognition.compare_faces(stored_encodings, new_encoding, tolerance=0.5)
        if True in results:
            match_index = results.index(True)
            return photo_names[match_index], "Match found."

    return None, "No match found."

@app.route('/compare', methods=['POST'])
def compare():
    """
    API endpoint to compare an uploaded photo with stored photos.
    """
    if 'photo' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['photo']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        new_image = face_recognition.load_image_file(file)
        matched_photo, message = compare_photo(new_image)

        if matched_photo:
            return jsonify({"matched_photo": matched_photo, "message": message}), 200
        else:
            return jsonify({"message": message}), 200
    except Exception as e:
        logging.error(f"Error comparing photo: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5001)
