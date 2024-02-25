
import cv2 as cv

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2



GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


base_options = python.BaseOptions(model_asset_path='HandGesture\\gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

cam = cv.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cam.read()

    if not ret:
        print("error in retrieving frame")
        break
        
        
    rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    recognition_result = recognizer.recognize(rgb_frame)

    try:
        top_gesture = recognition_result.gestures[0][0]
    except IndexError:

        top_gesture = None

    hand_landmarks = recognition_result.hand_landmarks

    if top_gesture:
        title = f"{top_gesture.category_name} ({top_gesture.score:.2f})"
        print(title)


    
cam.release()