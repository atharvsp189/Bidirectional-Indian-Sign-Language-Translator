# Indian Sign Language to Text

This directory contains the codebase for converting Indian Sign Language (ISL) gestures into text using computer vision and machine learning.

## Features

- **Gesture Recognition**: Uses MediaPipe for hand tracking and custom TensorFlow Lite models for classifying hand gestures.
- **Real-time Processing**: Captures video from webcam and processes frames in real-time.
- **Web Interface**: Provides a Flask-based web interface to view the live feed and recognized text.
- **Model Training**: Includes notebooks used for training the gesture recognition models.

## Usage

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Application**:
    ```bash
    python app.py
    ```

3.  **Access the Interface**:
    Open your browser and navigate to `http://localhost:5000` (or the port displayed in the console).

## Directory Structure

*   **app.py**: The main Flask application that handles video streaming and gesture recognition logic.
*   **model/**: Contains the pre-trained models and classifier classes.
    *   **keypoint_classifier/**: Hand gesture classifier model (`.tflite`, labels, processing logic).
    *   **point_history_classifier/**: Finger gesture history classifier.
*   **utils/**: Utility scripts, e.g., `cvfpscalc.py` for calculating FPS.
*   **templates/**: HTML templates for the Flask app.
*   **Notebooks/**: Jupyter notebooks used for data preprocessing and model training.

## How it Works

1.  **Hand Detection**: MediaPipe Hands is used to detect hand landmarks (21 points) from the video frame.
2.  **Feature Extraction**: The relative coordinates of these landmarks are extracted and normalized.
3.  **Classification**: These features are fed into a TFLite model (`KeyPointClassifier`) which predicts the sign/gesture class.
4.  **Display**: The recognized gesture and confidence score are overlaid on the video feed.
