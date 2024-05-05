import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import random

def load_model_and_predict(file_path):
    # Load the model to detect CT scans or X-rays
    # Load the model to detect CT scans or X-rays
    ct_xray_model_path = r'models/ct_xray_classifier.keras'
    if not os.path.exists(ct_xray_model_path):
        raise ValueError('Model file for CT scan and X-ray detection not found.')
    ct_xray_model = tf.keras.models.load_model(ct_xray_model_path)

    # Load the image and preprocess it
    img = image.load_img(file_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.

    # Predict whether the image is a CT scan or an X-ray
    ct_xray_prediction = ct_xray_model.predict(img_array)
    is_ct_scan = ct_xray_prediction[0][0] > 0.5

    if is_ct_scan:
        print("CT scan detected")
        selected_model_path = r'models/lungCancerV3_model.keras'
        model = tf.keras.models.load_model(selected_model_path)
        prediction = model.predict(img_array)
        confidence = prediction[0][0] * 100
        if confidence > 50:
            predicted_class = 'No Lung Cancer'
        else:
            predicted_class = 'Lung Cancer'
        return predicted_class
    else:
        print("X-ray detected")
        selected_model_path = r'models/tb-pneumonia_model.keras'
         # Load the selected model
        if not os.path.exists(selected_model_path):
            raise ValueError(f'Model file for disease detection not found: {selected_model_path}')
        selected_model = tf.keras.models.load_model(selected_model_path)
        class_names = ['TB', 'No TB', 'No Pneumonia', 'Pneumonia']
        img = image.load_img(file_path, target_size=(299, 299))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.inception_v3.preprocess_input(img_array)
        predictions = selected_model.predict(img_array)
        predicted_class = class_names[np.argmax(predictions)]
        return predicted_class
