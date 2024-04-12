import os
import sys
REPO_DIR_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.append(REPO_DIR_PATH)

import cv2
from src.image_preprocessing import ImagePreprocessing
from src.exception import CustomException
from src.logger import logging


class VisualizeMovements(ImagePreprocessing):
    def __init__(self):
        super().__init__()

    def visualize(self):
        """
        This function will visualize the movements.
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
            cond = True
            center_y = 0
            counter = 0
            number_of_frames = 15

            # Loop to capture and process video frames
            while True:
                # Read a frame from the video capture device
                ret, frame = cap.read()
                # Check if frame is successfully read
                if not ret:
                    break
                # Get the frame height
                frame_height, _, _ = frame.shape
                # Flip the frame horizontally for natural (selfie-view) visualization
                frame = cv2.flip(frame, 1)
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
                        # Increment counter if hands are joined
                        counter += 1
                        color = (0, 255, 0)
                        # Display "Hands Joined" status on the frame
                        cv2.putText(frame, hand_joined_status, (10, 30),
                                    cv2.FONT_HERSHEY_PLAIN, 2, color, 3)
                    elif hand_joined_status == "Hands Not Joined":
                        # Reset counter if hands are not joined
                        counter = 0
                        color = (0, 0, 255)
                        # Display "Hands Not Joined" status on the frame
                        cv2.putText(frame, hand_joined_status, (10, 30),
                                    cv2.FONT_HERSHEY_PLAIN, 2, color, 3)

                    # Check if initial shoulder coordinates need to be calculated
                    if cond and counter == number_of_frames:
                        initial_shoulder_coordinates = self.get_initial_shoulder_coordinates(
                            frame, results)
                        y_right = initial_shoulder_coordinates["right_shoulder"][1]
                        y_left = initial_shoulder_coordinates["left_shoulder"][1]
                        center_y = (y_right + y_left)//2
                        cond = False
                    # If initial shoulder coordinates are already calculated
                    elif not cond:
                        frame_height, frame_width, _ = frame.shape

                        # Draw horizontal and vertical lines on the frame
                        frame = self.draw_horizontal_and_vertical_lines(
                            frame, center_y)

                        # Check if left-right movement is detected
                        horizontal_status = self.check_left_right(
                            frame, results)
                        if horizontal_status is not None:
                            # Display left-right movement status on the frame
                            cv2.putText(frame, horizontal_status, (5, frame_height - 10),
                                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

                        # Check if up-down movement is detected
                        vertical_status = self.check_up_down(
                            frame, center_y, results)
                        if vertical_status is not None:
                            # Display up-down movement status on the frame
                            cv2.putText(frame, vertical_status, (frame_width-150, frame_height - 10),
                                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
                    else:
                        # Display message to join both hands to start visualizing movements
                        cv2.putText(frame, 'Join Both Hands to start visualizing movements', (5, frame_height - 10), cv2.FONT_HERSHEY_PLAIN,
                                    2, (0, 255, 0), 3)

                # Display the frame in the named window
                cv2.imshow("feed", frame)

                # Check for key press to exit the loop
                if cv2.waitKey(10) & 0xff == ord('q'):
                    break

            # Release video capture device and close all windows
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            logging.error(f"Error visualizing movements: {e}")
            raise CustomException("Error visualizing movements", sys)


if __name__ == "__main__":
    visualize = VisualizeMovements()
    visualize.visualize()
