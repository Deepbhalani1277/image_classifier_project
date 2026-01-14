// ============================================
// CNN IMAGE CLASSIFIER - JAVASCRIPT
// Handles image upload, preview, and classification
// ============================================

// ============================================
// GLOBAL VARIABLES
// ============================================
let selectedFile = null;

// Icon mapping for each class
const classIcons = {
    'airplane': 'fa-plane',
    'automobile': 'fa-car',
    'bird': 'fa-dove',
    'cat': 'fa-cat',
    'deer': 'fa-horse',  // Font Awesome doesn't have deer, using horse
    'dog': 'fa-dog',
    'frog': 'fa-frog',
    'horse': 'fa-horse',
    'ship': 'fa-ship',
    'truck': 'fa-truck'
};


// ============================================
// WAIT FOR PAGE TO LOAD
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Page loaded successfully!');
    
    // Only initialize if we're on the classify page
    if (document.getElementById('uploadArea')) {
        initializeClassifyPage();
    }
});


// ============================================
// INITIALIZE CLASSIFY PAGE
// ============================================
function initializeClassifyPage() {
    console.log('📋 Initializing classification page...');
    
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const classifyBtn = document.getElementById('classifyBtn');
    const tryAnotherBtn = document.getElementById('tryAnotherBtn');
    
    // File input change event
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop events
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Click to upload
    uploadArea.addEventListener('click', function(e) {
        if (e.target.id !== 'fileInput' && !e.target.closest('.change-image-btn')) {
            fileInput.click();
        }
    });
    
    // Classify button click
    if (classifyBtn) {
        classifyBtn.addEventListener('click', classifyImage);
    }
    
    // Try another button click
    if (tryAnotherBtn) {
        tryAnotherBtn.addEventListener('click', resetPage);
    }
    
    console.log('✅ Classification page initialized!');
}


// ============================================
// FILE SELECTION HANDLER
// ============================================
function handleFileSelect(event) {
    const file = event.target.files[0];
    
    if (file) {
        console.log('📁 File selected:', file.name);
        
        // Validate file type
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp'];
        
        if (!validTypes.includes(file.type)) {
            showError('Invalid file type. Please upload a JPG, PNG, GIF, or BMP image.');
            return;
        }
        
        // Validate file size (max 16MB)
        const maxSize = 16 * 1024 * 1024; // 16MB in bytes
        if (file.size > maxSize) {
            showError('File too large. Maximum size is 16MB.');
            return;
        }
        
        selectedFile = file;
        displayImagePreview(file);
    }
}


// ============================================
// DRAG AND DROP HANDLERS
// ============================================
function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    event.currentTarget.classList.add('drag-over');
}

function handleDragLeave(event) {
    event.preventDefault();
    event.stopPropagation();
    event.currentTarget.classList.remove('drag-over');
}

function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    event.currentTarget.classList.remove('drag-over');
    
    const files = event.dataTransfer.files;
    
    if (files.length > 0) {
        const file = files[0];
        console.log('📁 File dropped:', file.name);
        
        // Validate file type
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp'];
        
        if (!validTypes.includes(file.type)) {
            showError('Invalid file type. Please upload a JPG, PNG, GIF, or BMP image.');
            return;
        }
        
        selectedFile = file;
        
        // Update file input
        const fileInput = document.getElementById('fileInput');
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;
        
        displayImagePreview(file);
    }
}


// ============================================
// DISPLAY IMAGE PREVIEW
// ============================================
function displayImagePreview(file) {
    console.log('🖼️ Displaying image preview...');
    
    const uploadContent = document.getElementById('uploadContent');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const actionButtons = document.getElementById('actionButtons');
    
    // Read file and display
    const reader = new FileReader();
    
    reader.onload = function(e) {
        previewImg.src = e.target.result;
        
        // Hide upload content, show preview
        uploadContent.style.display = 'none';
        imagePreview.style.display = 'block';
        actionButtons.style.display = 'block';
        
        console.log('✅ Image preview displayed!');
    };
    
    reader.readAsDataURL(file);
}


// ============================================
// CLASSIFY IMAGE
// ============================================
async function classifyImage() {
    console.log('🔍 Starting image classification...');
    
    if (!selectedFile) {
        showError('Please select an image first.');
        return;
    }
    
    // Hide action buttons and results
    document.getElementById('actionButtons').style.display = 'none';
    document.getElementById('resultsContainer').style.display = 'none';
    document.getElementById('errorContainer').style.display = 'none';
    
    // Show loading animation
    document.getElementById('loadingContainer').style.display = 'block';
    
    // Create form data
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    try {
        console.log('📤 Sending image to server...');
        
        // Send request to backend
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        console.log('📥 Received response:', data);
        
        if (data.success) {
            // Hide loading, show results
            document.getElementById('loadingContainer').style.display = 'none';
            displayResults(data);
        } else {
            // Show error
            document.getElementById('loadingContainer').style.display = 'none';
            showError(data.error || 'Classification failed. Please try again.');
        }
        
    } catch (error) {
        console.error('❌ Error during classification:', error);
        document.getElementById('loadingContainer').style.display = 'none';
        showError('Network error. Please check your connection and try again.');
    }
}


// ============================================
// DISPLAY RESULTS
// ============================================
function displayResults(data) {
    console.log('📊 Displaying results...');
    
    const resultsContainer = document.getElementById('resultsContainer');
    const predictionIcon = document.getElementById('predictionIcon');
    const predictedClass = document.getElementById('predictedClass');
    const confidenceValue = document.getElementById('confidenceValue');
    const confidenceFill = document.getElementById('confidenceFill');
    const predictionsList = document.getElementById('predictionsList');
    const predictionsChart = document.getElementById('predictionsChart');
    
    // Update main prediction
    const iconClass = classIcons[data.predicted_class] || 'fa-question';
    predictionIcon.innerHTML = `<i class="fas ${iconClass}"></i>`;
    predictedClass.textContent = data.predicted_class;
    confidenceValue.textContent = `${data.confidence}%`;
    
    // Animate confidence bar
    setTimeout(() => {
        confidenceFill.style.width = `${data.confidence}%`;
    }, 100);
    
    // Display top 3 predictions
    predictionsList.innerHTML = '';
    data.top_3_predictions.forEach((pred, index) => {
        const item = document.createElement('div');
        item.className = 'prediction-item';
        item.style.animationDelay = `${index * 0.1}s`;
        item.innerHTML = `
            <span class="prediction-name">
                <i class="fas ${classIcons[pred.class] || 'fa-question'}"></i>
                ${pred.class}
            </span>
            <span class="prediction-confidence">${pred.confidence.toFixed(2)}%</span>
        `;
        predictionsList.appendChild(item);
    });
    
    // Display all predictions chart
    predictionsChart.innerHTML = '';
    const sortedPredictions = Object.entries(data.all_predictions)
        .sort((a, b) => b[1] - a[1]);
    
    sortedPredictions.forEach(([className, confidence], index) => {
        const chartItem = document.createElement('div');
        chartItem.className = 'chart-item';
        chartItem.style.animationDelay = `${index * 0.05}s`;
        chartItem.innerHTML = `
            <div class="chart-label">${className}</div>
            <div class="chart-bar-container">
                <div class="chart-bar" style="width: 0%;" data-width="${confidence}%"></div>
            </div>
            <div class="chart-value">${confidence.toFixed(1)}%</div>
        `;
        predictionsChart.appendChild(chartItem);
    });
    
    // Animate chart bars
    setTimeout(() => {
        document.querySelectorAll('.chart-bar').forEach(bar => {
            bar.style.width = bar.getAttribute('data-width');
        });
    }, 100);
    
    // Show results container
    resultsContainer.style.display = 'block';
    
    console.log('✅ Results displayed successfully!');
}


// ============================================
// SHOW ERROR
// ============================================
function showError(message) {
    console.error('❌ Error:', message);
    
    const errorContainer = document.getElementById('errorContainer');
    const errorMessage = document.getElementById('errorMessage');
    const loadingContainer = document.getElementById('loadingContainer');
    const actionButtons = document.getElementById('actionButtons');
    
    // Hide loading and action buttons
    if (loadingContainer) loadingContainer.style.display = 'none';
    if (actionButtons) actionButtons.style.display = 'none';
    
    // Show error
    errorMessage.textContent = message;
    errorContainer.style.display = 'block';
}


// ============================================
// RESET PAGE
// ============================================
function resetPage() {
    console.log('🔄 Resetting page...');
    
    // Reset file input
    document.getElementById('fileInput').value = '';
    selectedFile = null;
    
    // Reset UI
    document.getElementById('uploadContent').style.display = 'block';
    document.getElementById('imagePreview').style.display = 'none';
    document.getElementById('actionButtons').style.display = 'none';
    document.getElementById('loadingContainer').style.display = 'none';
    document.getElementById('resultsContainer').style.display = 'none';
    document.getElementById('errorContainer').style.display = 'none';
    
    console.log('✅ Page reset complete!');
}


// ============================================
// SMOOTH SCROLL FOR NAVIGATION
// ============================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});


// ============================================
// ADD ENTRANCE ANIMATIONS
// ============================================
window.addEventListener('load', function() {
    // Add fade-in class to elements
    const elements = document.querySelectorAll('.hero-content > *, .classify-container > *');
    elements.forEach((el, index) => {
        setTimeout(() => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            
            setTimeout(() => {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }, 50);
        }, index * 100);
    });
});


// ============================================
// CONSOLE WELCOME MESSAGE
// ============================================
console.log('%c🧠 CNN Image Classifier', 'font-size: 24px; font-weight: bold; color: #667eea;');
console.log('%cBuilt with TensorFlow, Flask, and ❤️', 'font-size: 14px; color: #888;');
console.log('%cCollege Project - CSUP201 SGP - 2026', 'font-size: 12px; color: #666;');
