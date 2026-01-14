# 🧠 CNN Image Classifer

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.16.1-orange.svg)](https://tensorflow.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A powerful **Deep Learning** web application that classifies images into 10 distinct categories using a Convolutional Neural Network (CNN). Built with TensorFlow, Keras, and Flask.

---

## 🚀 Features

- **High Accuracy:** ~85% accuracy on CIFAR-10 test dataset.
- **Real-time Prediction:** Instant classification with confidence scores.
- **Interactive UI:** Modern, responsive web interface with drag-and-drop upload.
- **Visual Analytics:** Probability charts and top-3 predictions.
- **Fast Training:** Optimized for GPU training on Google Colab.

## 📂 Project Structure

```
├── app.py                 # Flask/Backend Logic
├── train_model.py         # CNN Training Script
├── model.h5               # Trained Model File
├── CNN_Training.ipynb     # Google Colab Notebook
├── requirements.txt       # Dependencies
├── static/                # CSS, JS, Images
├── templates/             # HTML Templates
└── docs/
    └── PRESENTATION_SCRIPT.md  # Script for Project Demo
```

## 🛠️ Technology Stack

- **Deep Learning:** TensorFlow (2.16.1), Keras
- **Backend:** Flask, Python 3.10
- **Frontend:** HTML5, CSS3, JavaScript
- **Data:** CIFAR-10 Dataset (60,000 images)

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/cnn-image-classifier.git
cd cnn-image-classifier
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```
Open **http://127.0.0.1:5000** in your browser.

## 🎓 Presentation

We have included a complete script for demonstrating this project:
- **[Presentation Script](docs/PRESENTATION_SCRIPT.md)**

## 👥 Contributors

- **Deep Bhalani** (D25DCS165)
- **Vishwa Vaghasiya** (D25DCS154)

---
*Created for CSUP201 SGP - 4th Semester B.Tech (2026)*
