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

def determine_action(gesture, direction, handedness):
    print(gesture,direction,handedness)
    if gesture == 'Closed_Fist':
        if handedness == 'Right':
            if direction == 'Up':
                print('Action_A')
            elif direction == 'Down':
                print('Action_B')
            elif direction == 'Left':
                print('Action_C')
            elif direction == 'Right':
                print('Action_D')
            else:
                print('Invalid direction')
        else:
            if direction == 'Up':
                print('Action_E')
            elif direction == 'Down':
                print('Action_F')
            elif direction == 'Left':
                print('Action_G')
            elif direction == 'Right':
                print('Action_H')
            else:
                print('Invalid direction')
        
    elif gesture == 'Victory':
        if handedness == 'Right':
            if direction == 'Up':
                print('Action_I')
            elif direction == 'Down':
                print('Action_J')
            elif direction == 'Left':
                print('Action_K')
            elif direction == 'Right':
                print('Action_L')
            else:
                print('Invalid direction')
        else:
            if direction == 'Up':
                print('Action_M')
            elif direction == 'Down':
                print('Action_N')
            elif direction == 'Left':
                print('Action_O')
            elif direction == 'Right':
                print('Action_P')
            else:
                print('Invalid direction')
        
    elif gesture == 'Pointing_Up':
        if handedness == 'Right':
            if direction == 'Up':
                print('Action_Q')
            elif direction == 'Down':
                print('Action_R')
            elif direction == 'Left':
                print('Action_S')
            elif direction == 'Right':
                print('Action_T')
            else:
                print('Invalid direction')
        else:
            if direction == 'Up':
                print('Action_U')
            elif direction == 'Down':
                print('Action_V')
            elif direction == 'Left':
                print('Action_W')
            elif direction == 'Right':
                print('Action_X')
            else:
                print('Invalid direction')
        
    elif gesture == 'Thumb_Up':
        if handedness == 'Right':
            if direction == 'Up':
                print('Action_Y')
            elif direction == 'Down':
                print('Action_Z')
            elif direction == 'Left':
                print('Action_1')
            elif direction == 'Right':
                print('Action_2')
            else:
                print('Invalid direction')
        else:
            if direction == 'Up':
                print('Action_3')
            elif direction == 'Down':
                print('Action_4')
            elif direction == 'Left':
                print('Action_5')
            elif direction == 'Right':
                print('Action_6')
            else:
                print('Invalid direction')
        
    else:
        print('Invalid gesture')


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
last_valid_sign = None
x_cords = [0] * 21
y_cords = [0] * 21
lost = False
majority_guess = 'None'
with GestureRecognizer.create_from_options(options) as recognizer, mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5) as hands:
    avg_handedness = [] 
    while True: #need a while True loop because program is continuosuly grabbing input from camera until user ends the program
        if len(avg_handedness) >= 100:
            avg_handedness = []
        #array to save each hand's landmarks
        prev_x = x_cords
        prev_y = y_cords
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
            avg_handedness.append(hand_type)
            for eachHand in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(frame, eachHand,mp.solutions.hands.HAND_CONNECTIONS)
                for landmark in eachHand.landmark:
                    x_cords.append(landmark.x)
                    y_cords.append(landmark.y)

            # if any(x < 0 or x > 1 or y < 0 or y > 1 for x, y in zip(x_cords, y_cords)):
            #     print("Hand outside the screen!")
            
            last_guesses.append(current_gesture_label)
            if len(last_guesses) > 5:
                last_guesses.pop(0)  

            if current_gesture_label in valid_signs:
                last_valid_sign = current_gesture_label

            majority_guess = max(set(last_guesses), key=last_guesses.count)

            avg_x = np.mean(x_cords)
            avg_y = np.mean(y_cords)
            hand = max(set(avg_handedness), key = avg_handedness.count)
            # print(current_gesture_label)
            if majority_guess in valid_signs and accepting_gesture:
                if avg_x < 0.25:
                    # print(majority_guess, "moved right", handedness)
                    determine_action(majority_guess, "Right", hand)
                    accepting_gesture = False
                elif avg_x > .75:
                    # print(majority_guess, "moved left", hand)
                    determine_action(majority_guess, "Left", hand)
                    accepting_gesture = False
                if avg_y < 0.25:
                    # print(majority_guess, "moved up", hand)
                    determine_action(majority_guess, "Up", hand)
                    accepting_gesture = False
                elif avg_y > .75:
                    # print(majority_guess, "moved down", hand)
                    determine_action(majority_guess, "Down", hand)
                    accepting_gesture = False
                majority_guess = 'None'
                last_guesses = []

            if .4 <= avg_x <= .6 and .4 <= avg_y <= .6 and accepting_gesture == False:
                accepting_gesture = True
                avg_handedness = []
                print('centered')
        else:
            if accepting_gesture and last_valid_sign is not None:
                leftmost_x = min(prev_x)
                rightmost_x = max(prev_x)
                topmost_y = min(prev_y)
                bottommost_y = max(prev_y)

                x = (leftmost_x + rightmost_x) / 2
                y = (topmost_y + bottommost_y) / 2

                if not (.4 <= x <= .6 and .4 <= y <= .6):
                    if x < .5:
                        distance_x = x
                        if y < .5:
                            distance_y = y
                            if distance_y < distance_x:
                                # print(last_valid_sign, "closest up", hand)
                                determine_action(last_valid_sign, "Up", hand)
                                accepting_gesture = False
                            else:
                                # print(last_valid_sign, "closest right", hand)
                                determine_action(last_valid_sign, "Right", hand)

                                accepting_gesture = False
                        else:
                            distance_y = 1 - y 
                            if distance_y < distance_x:
                                # print(last_valid_sign, "closest down", hand)
                                determine_action(last_valid_sign, "Down", hand)
                                accepting_gesture = False
                            else:
                                # print(last_valid_sign, "closest right", hand)
                                determine_action(last_valid_sign, "Right", hand)
                                accepting_gesture = False
                    else:
                        distance_x = 1 - x
                        if y < .5:
                            distance_y = y
                            if distance_y < distance_x:
                                # print(last_valid_sign, "closest up", hand)
                                determine_action(last_valid_sign, "Up", hand)
                                accepting_gesture = False
                            else:
                                # print(last_valid_sign, "closest left", hand)
                                determine_action(last_valid_sign, "Left", hand)
                                accepting_gesture = False
                        else:
                            distance_y = 1 - y 
                            if distance_y < distance_x:
                                # print(last_valid_sign, "closest down", hand)
                                determine_action(last_valid_sign, "Down", hand)
                                accepting_gesture = False
                            else:
                                # print(last_valid_sign, "closest left", hand)
                                determine_action(last_valid_sign, "Left", hand)
                                accepting_gesture = False  
                else:
                    accepting_gesture = False
            

        cv2.imshow('Window', frame)
        
        #esc key will end the program
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

    