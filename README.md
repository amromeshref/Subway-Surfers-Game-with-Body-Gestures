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

## How It Works

The application works by capturing video frames from the webcam, processing them using pose detection algorithms, and interpreting the detected poses to control the Subway Surfers game. Here's how it works:

1. **Image Preprocessing**: The `image_processing.py` script preprocesses each frame to detect poses and analyze movements.
   
2. **Pose Detection**: The application uses the MediaPipe library to detect key body landmarks such as shoulders, wrists, and joints in each frame.
   
3. **Interpreting Movements**: Based on the detected poses, the application determines the player's movements, such as whether their hands are joined, if they are moving left, right, up, or down.

4. **Controlling the Game**: Using PyAutoGUI, the application simulates keyboard inputs (such as pressing the spacebar, arrow keys) to control the Subway Surfers game, translating the detected movements into in-game actions.
