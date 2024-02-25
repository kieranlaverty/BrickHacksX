# STEP 1: Import the necessary modules.
import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# STEP 2: Create an GestureRecognizer object.
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
    # STEP 4: Recognize gestures in the input image.
    recognition_result = recognizer.recognize(rgb_frame)
    #print(recognition_result)

    # prompt: recognition_result.gestures[0][0] is giving me an index error

    try:
        top_gesture = recognition_result.gestures[0][0]
    except IndexError:
        # Handle the case where there are no gestures detected
        print("No gestures detected in the image.")
        top_gesture = None

    hand_landmarks = recognition_result.hand_landmarks

    # hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    # hand_landmarks_proto.landmark.extend([
    #     landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
    #     ])

    # STEP 5: Process the result. In this case, visualize it.
    if top_gesture:
        title = f"{top_gesture.category_name} ({top_gesture.score:.2f})"
        print(title)

    # if hand_landmarks:
    #         for hand_landmark in hand_landmarks:
    #            mp_drawing.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)
    #            if top_gesture:
    #                mp_drawing.draw_landmarks(top_gesture, hand_landmark, mp_hands.HAND_CONNECTIONS)
    
cam.release()