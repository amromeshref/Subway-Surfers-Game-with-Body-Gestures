# Playing Subway Surfers Game using Pose Detection

This project integrates pose detection using MediaPipe to control movements in the Subway Surfers game. Users can interact with the game using their body movements detected through a camera.

## Introduction

This repository contains two Python scripts:

- **image_processing.py**: Handles image preprocessing tasks related to pose detection and movement analysis.
- **app.py**: Runs the application, capturing video frames from the webcam, processing them for pose detection, and simulating keyboard inputs to control the game based on detected movements.

## Requirements

Before running the scripts, ensure you have the following dependencies installed:

- Python 3.x
- OpenCV
- MediaPipe
- PyAutoGUI

You can install the dependencies using pip:


## Usage

1. Clone the repository:

2. Navigate to the project directory:

3. Run the application:




## Functionality

- **ImagePreprocessing Class (image_processing.py)**: Handles image preprocessing tasks such as getting initial shoulder coordinates, drawing lines on the frame, calculating distances, and checking for hands joined, left-right movement, and up-down movement.

- **App Class (app.py)**: Inherits functionalities from ImagePreprocessing class and implements the main application logic. It captures video frames, processes them for pose detection, and simulates keyboard inputs based on detected movements to control the Subway Surfers game.

## Configuration

The configuration for this project is stored in a config file. You can adjust parameters such as minimum detection confidence, tracking confidence, line thresholds, and distance thresholds in the config file.

## Credits

This project was created by [Your Name]. It utilizes the MediaPipe library for pose detection and PyAutoGUI for simulating keyboard inputs.
