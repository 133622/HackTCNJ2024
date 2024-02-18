import pandas as pd
import os
import random
import numpy as np
import pickle
import cv2
import mediapipe as mp
import re

valid_signs = ['Closed_Fist', 'Victory', 'Pointing_Up', 'Thumb_Up']

current_gesture = None
model_path = 'C:/Users/bengu/Documents/GitHub/HackTCNJ2024/gesture_recognizer.task'

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode


video = cv2.VideoCapture(0)

# Create a image segmenter instance with the live stream mode:
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global current_gesture 
    current_gesture = result.gestures
    
timestamp = 0

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

     
#takes input from camera 
cap = cv2.VideoCapture(0)
cv2.namedWindow("Window", cv2.WND_PROP_AUTOSIZE)
cv2.setWindowProperty("Window", cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE)

#mediapipe functions
mpDraw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
last_guesses = []
accepting_gesture = True

with GestureRecognizer.create_from_options(options) as recognizer, mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5) as hands:
    while True: #need a while True loop because program is continuosuly grabbing input from camera until user ends the program

        #array to save each hand's landmarks
        x_cords = []
        y_cords = []
        #takes in a frame
        ret, frame = cap.read()
        if not ret:
            break

        timestamp += 1
        current_gesture_label = 'None'
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        # Send live image data to perform gesture recognition
        # The results are accessible via the `result_callback` provided in
        # the `GestureRecognizerOptions` object.
        # The gesture recognizer must be created with the live stream mode.
        recognizer.recognize_async(mp_image, timestamp)
        match = re.search(r"category_name='(\w+)'", str(current_gesture))
        if match:
            current_gesture_label = match.group(1)
        
        # print(current_gesture_label)
        frameChanged = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frameChanged)

        if results.multi_hand_landmarks != None: #if there is atleast one hand in the frame
            #for each hand the coordinates of the landmarks (21 of them) are saved in a list 
            #the list is appended to the earlier array
            hand_type = "Left "if (results.multi_handedness[0].classification[0].label == 'Right') else "Right"

            for eachHand in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(frame, eachHand,mp.solutions.hands.HAND_CONNECTIONS)
                for landmark in eachHand.landmark:
                    x_cords.append(landmark.x)
                    y_cords.append(landmark.y)

            # if any(x < 0 or x > 1 or y < 0 or y > 1 for x, y in zip(x_cords, y_cords)):
            #     print("Hand outside the screen!")

            last_guesses.append(current_gesture_label)
            if len(last_guesses) > 20:
                last_guesses.pop(0)  

            majority_guess = max(set(last_guesses), key=last_guesses.count)

            avg_x = np.mean(x_cords)
            avg_y = np.mean(y_cords)

            if majority_guess in valid_signs and accepting_gesture:
                if avg_x < 0.1:
                    print(majority_guess, "moved right")
                    accepting_gesture = False

                elif avg_x > .9:
                    print(majority_guess, "moved left")
                    accepting_gesture = False

                if avg_y < 0.1:
                    print(majority_guess, "moved up")
                    accepting_gesture = False

                elif avg_y > .9:
                    print(majority_guess, "moved down")
                    accepting_gesture = False
                majority_guess = 'None'
                last_guesses = []

            
            if .3 <= avg_x <= .7 and .3 <= avg_y <= .7 and accepting_gesture == False:
                accepting_gesture = True
                print('centered')
                

        cv2.imshow('Window', frame)
        
        #esc key will end the program
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

    