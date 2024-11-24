from flask import Flask, request, render_template, jsonify
import os
from pathlib import Path  # Import Path
from detection import detect_products
from grouping import group_products

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Step 1: Detect products
    detections, detected_img_path = detect_products(filepath, RESULT_FOLDER)

    # Step 2: Group products
    clusters, grouped_img_path = group_products(detections, RESULT_FOLDER)

    # Convert file paths to strings (if they are Path objects)
    detected_img_path_str = str(detected_img_path)  # Convert Path to string
    grouped_img_path_str = str(grouped_img_path)    # Convert Path to string

    # Response JSON
    response = {
        "detections": detections,
        "clusters": clusters,
        "detected_image": detected_img_path_str,  # Use string paths here
        "grouped_image": grouped_img_path_str     # Use string paths here
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
