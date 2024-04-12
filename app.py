import os
import sys
REPO_DIR_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.append(REPO_DIR_PATH)

import cv2
import pyautogui
from src.exception import CustomException
from src.logger import logging
from src.image_preprocessing import ImagePreprocessing


class App(ImagePreprocessing):
    def __init__(self):
        super().__init__()

    def run(self):
        """
        This function will run the application.
        """
        try:
            # Open video capture device (webcam)
            cap = cv2.VideoCapture(0)
            # Check if video capture device is opened successfully
            if not cap.isOpened():
                logging.error("Error opening video capture device")
                exit()
            # Set the width and height properties of the video capture device
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
            # Create a named window for displaying the video feed
            cv2.namedWindow("feed", cv2.WINDOW_NORMAL)

            # Initialize variables
            counter = 0
            number_of_frames = 15
            start_game = False
            center_y = 0
            prev_horizontal_status = None
            prev_vertical_status = None

            # Loop to capture and process video frames
            while True:
                # Read a frame from the video capture device
                ret, frame = cap.read()
                # Check if frame is successfully read
                if not ret:
                    break
                # Flip the frame horizontally for natural (selfie-view) visualization
                frame = cv2.flip(frame, 1)
                # Extract frame dimensions
                frame_height, frame_width, _ = frame.shape
                # Convert frame to RGB format
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Process frame using Pose model
                results = self.pose_model.process(frame_rgb)
                # Check if pose landmarks are detected
                if results.pose_landmarks is not None:
                    # Check if hands are joined
                    hand_joined_status = self.check_hands_joined(
                        frame, results)
                    if hand_joined_status == "Hands Joined":
                        # Display "Hands Joined" status on the frame
                        cv2.putText(frame, hand_joined_status, (10, 30),
                                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
                        counter += 1
                        # Check if hands have been joined for a certain number of frames
                        if counter == number_of_frames:
                            # If game has not started yet, start the game and initialize variables
                            if not start_game:
                                logging.info("Game started")
                                pyautogui.press("space")
                                start_game = True
                                initial_shoulder_coordinates = self.get_initial_shoulder_coordinates(
                                    frame, results)
                                y_right = initial_shoulder_coordinates["right_shoulder"][1]
                                y_left = initial_shoulder_coordinates["left_shoulder"][1]
                                center_y = (y_right + y_left)//2
                            # If game has already started, stop the game
                            else:
                                logging.info("Game stopped")
                                pyautogui.press("esc")
                            counter = 0
                    else:
                        # Display "Hands Not Joined" status on the frame
                        cv2.putText(frame, hand_joined_status, (10, 30),
                                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
                        counter = 0

                    # Draw horizontal and vertical lines on the frame if the game has started
                    if start_game:
                        frame = self.draw_horizontal_and_vertical_lines(
                            frame, center_y)

                    # Check for left-right movement
                    if start_game:
                        # Get the horizontal movement status
                        horizontal_status = self.check_left_right(
                            frame, results)
                        # Display left-right movement status on the frame
                        cv2.putText(frame, horizontal_status, (5, frame_height - 10),
                                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
                        # If the movement status has changed, simulate corresponding keyboard input
                        if horizontal_status != prev_horizontal_status:
                            if horizontal_status == "Center":
                                if prev_horizontal_status == "Left":
                                    logging.info("Move Right")
                                    pyautogui.press("right")
                                elif prev_horizontal_status == "Right":
                                    logging.info("Move Left")
                                    pyautogui.press("left")
                            if horizontal_status == "Left":
                                logging.info("Move Left")
                                pyautogui.press("left")
                            if horizontal_status == "Right":
                                logging.info("Move Right")
                                pyautogui.press("right")
                            prev_horizontal_status = horizontal_status

                    # Check for up-down movement
                    if start_game:
                        # Get the vertical movement status
                        vertical_status = self.check_up_down(
                            frame, center_y, results)
                        # Display up-down movement status on the frame
                        cv2.putText(frame, vertical_status, (frame_width-150, frame_height - 10),
                                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
                        # If the movement status has changed, simulate corresponding keyboard input
                        if vertical_status != prev_vertical_status:
                            if vertical_status == "Up":
                                logging.info("Move Up")
                                pyautogui.press("up")
                            if vertical_status == "Down":
                                logging.info("Move Down")
                                pyautogui.press("down")
                            prev_vertical_status = vertical_status
                # Display the frame in the named window
                cv2.imshow("feed", frame)
                # Check for key press to exit the loop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            # Release video capture device and close all windows
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            logging.error(f"Error opening video capture device: {e}")
            raise CustomException("Error opening video capture device", sys)


if __name__ == "__main__":
    app = App()
    app.run()
