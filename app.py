# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image
import numpy as np
import os
import hashlib  # Added for password hashing

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Import steganography logic from image_processing.py
from image_processing import encode_message, decode_message

# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Endpoint for rendering the main page
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint for image encoding
@app.route('/encode', methods=['POST'])
def encode():
    try:
        # Get the uploaded image file
        uploaded_file = request.files['file']
        
        # Read the image as a Pillow Image object
        original_image = Image.open(uploaded_file)

        # Get the secret message and password from the request form
        secret_message = request.form['message']
        password = request.form['password']

         # Hash the password for security
        hashed_password = hash_password(password)

        # Encode the message into the image
        encoded_image = encode_message(original_image, secret_message, hashed_password)

        # Save the encoded image to the uploads folder
        filename = 'encoded_image.jpg'
        encoded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        encoded_image.save(encoded_image_path)

        return jsonify({'success': True, 'message': 'Message encoded successfully', 'encoded_image_path': filename})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Endpoint for image decoding
@app.route('/decode', methods=['POST'])
def decode():
    try:
        # Get the uploaded image file
        uploaded_file = request.files['file']

        # Get the password from the request form
        password = request.form['password']

        # Hash the password for security
        hashed_password = hash_password(password)

        # Read the image as a Pillow Image object
        encoded_image = Image.open(uploaded_file)

        # Decode the message from the image
        decoded_message = decode_message(encoded_image, hashed_password)

        return jsonify({'success': True, 'message': 'Message decoded successfully', 'decoded_message': decoded_message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Endpoint to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
