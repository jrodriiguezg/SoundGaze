import cv2  # type: ignore
import numpy as np
import dlib
import math
import time

def facetracker(callback_function):
    """
    Detects faces, calculates head direction in degrees (yaw, pitch),
    and tracks head movements in the background.

    Does not display the camera feed in a window.
    Calls the callback function with movement data.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    # Initialize the dlib landmark detector
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    if predictor is None:
        print("Error: Could not load the landmark predictor.")
        cap.release()
        return

    # Variables for movement tracking
    prev_yaw = None
    prev_pitch = None
    movimiento_yaw = "Center"
    movimiento_pitch = "Center"

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not capture a frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces using dlib's detector
        faces = detector(gray, 1)

        for face in faces:
            # Detect landmarks
            landmarks = predictor(gray, face)

            # Extract eye and nose points
            left_eye_left_corner = (landmarks.part(36).x, landmarks.part(36).y)
            left_eye_right_corner = (landmarks.part(39).x, landmarks.part(39).y)
            right_eye_left_corner = (landmarks.part(42).x, landmarks.part(42).y)
            right_eye_right_corner = (landmarks.part(45).x, landmarks.part(45).y)
            nose_tip = (landmarks.part(30).x, landmarks.part(30).y)

            # Calculate the center of the eyes
            eyes_center_x = (left_eye_left_corner[0] + left_eye_right_corner[0] + right_eye_left_corner[0] + right_eye_right_corner[0]) // 4
            eyes_center_y = (left_eye_left_corner[1] + left_eye_right_corner[1] + right_eye_left_corner[1] + right_eye_right_corner[1]) // 4
            eyes_center = (eyes_center_x, eyes_center_y)

            # Calculate the yaw angle (horizontal rotation)
            yaw = math.atan2(nose_tip[0] - eyes_center[0], nose_tip[1] - eyes_center[1])
            yaw = math.degrees(yaw)

            # Calculate the pitch angle (vertical rotation)
            pitch = math.atan2(nose_tip[1] - eyes_center[1], 1)
            pitch = math.degrees(pitch)

            # Track movement (based on angle changes)
            if prev_yaw is not None and prev_pitch is not None:
                diff_yaw = yaw - prev_yaw
                diff_pitch = pitch - prev_pitch

                if diff_yaw > 5:
                    movimiento_yaw = "Right"
                elif diff_yaw < -5:
                    movimiento_yaw = "Left"
                else:
                    movimiento_yaw = "Center"

                if diff_pitch > 5:
                    movimiento_pitch = "Down"
                elif diff_pitch < -5:
                    movimiento_pitch = "Up"
                else:
                    movimiento_pitch = "Center"
            
            # Update previous angles
            prev_yaw = yaw
            prev_pitch = pitch
            
            # Call the callback function with movement data
            callback_function(yaw, pitch, movimiento_yaw, movimiento_pitch)

        # Wait some time to avoid overloading the CPU (adjust as needed)
        time.sleep(0.1)

        # If the 'q' key is pressed, exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
