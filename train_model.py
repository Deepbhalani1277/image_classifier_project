"""
============================================
IMAGE CLASSIFICATION USING CNN
CIFAR-10 Dataset Training Script
============================================

This script trains a Convolutional Neural Network (CNN) to classify images
into 10 categories: airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck.

Author: College Project - 4th Semester B.Tech
Dataset: CIFAR-10 (60,000 images, 32x32 pixels)
"""

# ============================================
# STEP 1: IMPORT REQUIRED LIBRARIES
# ============================================
print("📦 Importing libraries...")

# TensorFlow and Keras for building the CNN
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical

# For numerical operations and data manipulation
import numpy as np

# For plotting graphs
import matplotlib.pyplot as plt
import seaborn as sns

# For confusion matrix
from sklearn.metrics import confusion_matrix, classification_report

print("✅ All libraries imported successfully!\n")


# ============================================
# STEP 2: LOAD CIFAR-10 DATASET
# ============================================
print("📥 Loading CIFAR-10 dataset...")
print("This may take a moment on first run (downloading ~170 MB)...\n")

# Load dataset - Keras automatically downloads it
# X_train: Training images (50,000 images)
# y_train: Training labels (50,000 labels)
# X_test: Testing images (10,000 images)
# y_test: Testing labels (10,000 labels)
(X_train, y_train), (X_test, y_test) = cifar10.load_data()

print(f"✅ Dataset loaded successfully!")
print(f"   Training images: {X_train.shape}")  # (50000, 32, 32, 3)
print(f"   Training labels: {y_train.shape}")  # (50000, 1)
print(f"   Testing images: {X_test.shape}")    # (10000, 32, 32, 3)
print(f"   Testing labels: {y_test.shape}\n")  # (10000, 1)

# Define class names for CIFAR-10
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
               'dog', 'frog', 'horse', 'ship', 'truck']


# ============================================
# STEP 3: DATA PREPROCESSING
# ============================================
print("🔧 Preprocessing data...")

# 3.1: Normalize pixel values from [0, 255] to [0, 1]
# Why? Neural networks work better with smaller values
X_train = X_train.astype('float32') / 255.0
X_test = X_test.astype('float32') / 255.0

# 3.2: Convert labels to one-hot encoding
# Example: Label 3 becomes [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
# Why? For categorical classification, we need this format
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

print("✅ Data preprocessing complete!")
print(f"   Image pixel range: [0.0, 1.0]")
print(f"   Labels shape: {y_train.shape}\n")


# ============================================
# STEP 4: BUILD CNN MODEL ARCHITECTURE
# ============================================
print("🏗️ Building CNN model architecture...\n")

model = models.Sequential([
    
    # ===== CONVOLUTIONAL BLOCK 1 =====
    # What it does: Detects basic features like edges, corners
    layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(32, 32, 3)),
    # 32 filters, 3x3 kernel size, ReLU activation
    # Input: 32x32x3 (RGB image) → Output: 32x32x32
    
    layers.BatchNormalization(),  # Normalizes activations (improves training)
    layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D((2, 2)),  # Reduces size: 32x32 → 16x16
    layers.Dropout(0.25),  # Randomly drops 25% neurons to prevent overfitting
    
    # ===== CONVOLUTIONAL BLOCK 2 =====
    # What it does: Detects more complex patterns (shapes, textures)
    layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    # 64 filters → Output: 16x16x64
    
    layers.BatchNormalization(),
    layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D((2, 2)),  # Reduces size: 16x16 → 8x8
    layers.Dropout(0.25),
    
    # ===== CONVOLUTIONAL BLOCK 3 =====
    # What it does: Detects high-level features (object parts)
    layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
    # 128 filters → Output: 8x8x128
    
    layers.BatchNormalization(),
    layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D((2, 2)),  # Reduces size: 8x8 → 4x4
    layers.Dropout(0.25),
    
    # ===== FLATTEN LAYER =====
    # Converts 3D feature maps to 1D vector
    # 4x4x128 = 2048 values in a single row
    layers.Flatten(),
    
    # ===== FULLY CONNECTED LAYERS =====
    # These layers make the final classification decision
    layers.Dense(256, activation='relu'),  # 256 neurons
    layers.BatchNormalization(),
    layers.Dropout(0.5),  # 50% dropout for strong regularization
    
    layers.Dense(128, activation='relu'),  # 128 neurons
    layers.Dropout(0.5),
    
    # ===== OUTPUT LAYER =====
    # 10 neurons (one for each class)
    # Softmax converts outputs to probabilities that sum to 1
    layers.Dense(10, activation='softmax')
])

# Display model architecture
model.summary()

print("\n✅ Model architecture created successfully!\n")


# ============================================
# STEP 5: COMPILE THE MODEL
# ============================================
print("⚙️ Compiling the model...")

model.compile(
    optimizer='adam',  # Adam optimizer (adaptive learning rate)
    loss='categorical_crossentropy',  # Loss function for multi-class classification
    metrics=['accuracy']  # Track accuracy during training
)

print("✅ Model compiled successfully!\n")


# ============================================
# STEP 6: TRAIN THE MODEL
# ============================================
print("🚀 Starting model training...")
print("This will take several minutes depending on your hardware.\n")

# Train the model
history = model.fit(
    X_train, y_train,
    batch_size=64,  # Process 64 images at a time
    epochs=10,  # Train for 50 complete passes through the dataset
    validation_data=(X_test, y_test),  # Validate on test data
    verbose=1  # Show progress bar
)

print("\n✅ Training complete!\n")


# ============================================
# STEP 7: EVALUATE THE MODEL
# ============================================
print("📊 Evaluating model performance...")

# Evaluate on test data
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)

print(f"\n✅ Test Accuracy: {test_accuracy * 100:.2f}%")
print(f"   Test Loss: {test_loss:.4f}\n")


# ============================================
# STEP 8: PLOT TRAINING HISTORY
# ============================================
print("📈 Generating accuracy and loss graphs...")

# Create figure with 2 subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Accuracy over epochs
ax1.plot(history.history['accuracy'], label='Training Accuracy', linewidth=2)
ax1.plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
ax1.set_title('Model Accuracy Over Time', fontsize=14, fontweight='bold')
ax1.set_xlabel('Epoch', fontsize=12)
ax1.set_ylabel('Accuracy', fontsize=12)
ax1.legend(loc='lower right')
ax1.grid(True, alpha=0.3)

# Plot 2: Loss over epochs
ax2.plot(history.history['loss'], label='Training Loss', linewidth=2)
ax2.plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
ax2.set_title('Model Loss Over Time', fontsize=14, fontweight='bold')
ax2.set_xlabel('Epoch', fontsize=12)
ax2.set_ylabel('Loss', fontsize=12)
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('training_history.png', dpi=300, bbox_inches='tight')
print("✅ Graphs saved as 'training_history.png'\n")
plt.show()


# ============================================
# STEP 9: CONFUSION MATRIX
# ============================================
print("🔍 Generating confusion matrix...")

# Make predictions on test data
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)  # Convert probabilities to class labels
y_true = np.argmax(y_test, axis=1)  # Convert one-hot to class labels

# Create confusion matrix
cm = confusion_matrix(y_true, y_pred_classes)

# Plot confusion matrix
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=class_names, yticklabels=class_names)
plt.title('Confusion Matrix', fontsize=16, fontweight='bold')
plt.xlabel('Predicted Label', fontsize=12)
plt.ylabel('True Label', fontsize=12)
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
print("✅ Confusion matrix saved as 'confusion_matrix.png'\n")
plt.show()

# Print classification report
print("📋 Classification Report:")
print(classification_report(y_true, y_pred_classes, target_names=class_names))


# ============================================
# STEP 10: SAVE THE MODEL
# ============================================
print("💾 Saving trained model...")

model.save('model.h5')

print("✅ Model saved as 'model.h5'")
print("\n" + "="*50)
print("🎉 TRAINING COMPLETE!")
print("="*50)
print("\nYou can now use this model in your Flask application.")
print("Next step: Run 'python app.py' to start the web server.\n")
