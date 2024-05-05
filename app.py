from flask import Flask, render_template, request, redirect, url_for,jsonify
from werkzeug.utils import secure_filename
import os
from inference import load_model_and_predict

app = Flask(__name__)

app.static_folder = 'static'

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Set the UPLOAD_FOLDER to an absolute path
app.config['UPLOAD_FOLDER'] = os.path.join(current_dir, 'uploads')

@app.route('/', methods=['GET', 'POST'])
def index():
      if request.method == 'POST':
        pass
      return render_template('front.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['image']
        
        if file:
            image_path = 'uploaded_image.png'  
            file.save(image_path)
            predicted_disease = load_model_and_predict(image_path)
            return jsonify({'disease': predicted_disease})
        else:
            return jsonify({'error': 'No image uploaded'}), 400
    return render_template('upload.html', predictions={})


