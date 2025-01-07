import os
from flask import Flask, request, jsonify
import face_recognition

app = Flask(__name__)

STORED_PHOTOS_DIR = "images"

def load_stored_photos():
    stored_encodings = []
    photo_names = []

    for file_name in os.listdir(STORED_PHOTOS_DIR):
        if file_name.endswith(('jpg', 'jpeg', 'png')):
            file_path = os.path.join(STORED_PHOTOS_DIR, file_name)
            image = face_recognition.load_image_file(file_path)
            try:
                encoding = face_recognition.face_encodings(image)[0]  
                stored_encodings.append(encoding)
                photo_names.append(file_name)
            except IndexError:
                print(f"Warning: No face found in {file_name}. Skipping.")

    return stored_encodings, photo_names

stored_encodings, photo_names = load_stored_photos()

def compare_photo(new_image):
    try:
        new_encoding = face_recognition.face_encodings(new_image)[0]
    except IndexError:
        return None, "No face detected in the new photo."

    results = face_recognition.compare_faces(stored_encodings, new_encoding)

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
        new_image = face_recognition.load_image_file(file)

        matched_photo, message = compare_photo(new_image)

        if matched_photo:
            return jsonify({"matched_photo": matched_photo, "message": message}), 200
        else:
            return jsonify({"message": message}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)