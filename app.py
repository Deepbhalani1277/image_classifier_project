"""
============================================
FLASK BACKEND SERVER
Image Classification Web Application
============================================

This Flask server handles:
1. Serving HTML pages
2. Accepting image uploads
3. Running CNN predictions
4. Returning results to frontend

Author: College Project - 4th Semester B.Tech
"""

# ============================================
# IMPORT REQUIRED LIBRARIES
# ============================================
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import os

# ============================================
# FLASK APP CONFIGURATION
# ============================================
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB file size


# ============================================
# LOAD TRAINED MODEL
# ============================================
print("🔄 Loading trained model...")
try:
    model = keras.models.load_model('model.h5')
    print("✅ Model loaded successfully!\n")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print("Please train the model first by running: python train_model.py\n")
    model = None


# ============================================
# CIFAR-10 CLASS NAMES
# ============================================
class_names = [
    'airplane', 'automobile', 'bird', 'cat', 'deer',
    'dog', 'frog', 'horse', 'ship', 'truck'
]


# ============================================
# HELPER FUNCTIONS
# ============================================

def allowed_file(filename):
    """
    Check if uploaded file has an allowed extension.
    
    Args:
        filename (str): Name of the uploaded file
    
    Returns:
        bool: True if extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_image(image_path):
    """
    Preprocess uploaded image for CNN prediction.
    
    Steps:
    1. Load image
    2. Resize to 32x32 pixels (CIFAR-10 size)
    3. Convert to RGB (in case of grayscale or RGBA)
    4. Convert to numpy array
    5. Normalize pixel values to [0, 1]
    6. Add batch dimension
    
    Args:
        image_path (str): Path to uploaded image
    
    Returns:
        numpy.ndarray: Preprocessed image ready for prediction
    """
    try:
        # Load image using PIL
        img = Image.open(image_path)
        
        # Convert to RGB (handles grayscale and RGBA images)
        img = img.convert('RGB')
        
        # Resize to 32x32 pixels (CIFAR-10 input size)
        img = img.resize((32, 32))
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Normalize pixel values from [0, 255] to [0, 1]
        img_array = img_array.astype('float32') / 255.0
        
        # Add batch dimension: (32, 32, 3) → (1, 32, 32, 3)
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None


# ============================================
# FLASK ROUTES
# ============================================

@app.route('/')
def home():
    """
    Home page route.
    Renders the landing page with project introduction.
    """
    return render_template('index.html')


@app.route('/classify')
def classify_page():
    """
    Classification page route.
    Renders the image upload and classification interface.
    """
    return render_template('classify.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Prediction API endpoint.
    
    Accepts image upload, processes it, runs CNN prediction,
    and returns the predicted class with confidence.
    
    Returns:
        JSON response with prediction results or error message
    """
    
    # Check if model is loaded
    if model is None:
        return jsonify({
            'success': False,
            'error': 'Model not loaded. Please train the model first.'
        }), 500
    
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file uploaded'
        }), 400
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected'
        }), 400
    
    # Check if file type is allowed
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': f'Invalid file type. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400
    
    try:
        # Save uploaded file securely
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Preprocess image
        processed_image = preprocess_image(filepath)
        
        if processed_image is None:
            return jsonify({
                'success': False,
                'error': 'Error processing image'
            }), 500
        
        # Make prediction
        predictions = model.predict(processed_image, verbose=0)
        
        # Get predicted class index
        predicted_class_index = np.argmax(predictions[0])
        
        # Get predicted class name
        predicted_class = class_names[predicted_class_index]
        
        # Get confidence (probability) for predicted class
        confidence = float(predictions[0][predicted_class_index]) * 100
        
        # Get top 3 predictions
        top_3_indices = np.argsort(predictions[0])[-3:][::-1]
        top_3_predictions = [
            {
                'class': class_names[i],
                'confidence': float(predictions[0][i]) * 100
            }
            for i in top_3_indices
        ]
        
        # Clean up: delete uploaded file (optional)
        # os.remove(filepath)
        
        # Return prediction results
        return jsonify({
            'success': True,
            'predicted_class': predicted_class,
            'confidence': round(confidence, 2),
            'top_3_predictions': top_3_predictions,
            'all_predictions': {
                class_names[i]: round(float(predictions[0][i]) * 100, 2)
                for i in range(len(class_names))
            }
        })
    
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({
            'success': False,
            'error': f'Prediction error: {str(e)}'
        }), 500


@app.route('/health')
def health_check():
    """
    Health check endpoint to verify server is running.
    """
    return jsonify({
        'status': 'running',
        'model_loaded': model is not None
    })


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(413)
def file_too_large(e):
    """Handle file size too large error."""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 16MB.'
    }), 413


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


# ============================================
# RUN THE APPLICATION
# ============================================
if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 STARTING FLASK SERVER")
    print("="*50)
    print("\n📱 Open your browser and go to:")
    print("   http://127.0.0.1:5000")
    print("\n⏹️  Press CTRL+C to stop the server\n")
    
    # Run Flask app
    # debug=True enables auto-reload when code changes
    app.run(debug=True, host='0.0.0.0', port=5000)
