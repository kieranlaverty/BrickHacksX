import mediapipe as mp
import cv2 as cv
import time
import threading

#trivia
import json
import requests




def current_milli_time():
    return round(time.time() * 1000)

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

globalResult = None
# Create a gesture recognizer instance with the live stream mode:
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    if result is not None:
        print('gesture recognition result: {}'.format(result.gestures))
    global globalResult
    globalResult = result

def getGesture(recognizer, frame):
    rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    thread = threading.Thread(target=recognizer.recognize_async, args=(rgb_frame, current_milli_time()))
    thread.start()
    thread.join()

    print(globalResult)

def printHandOutline(holisitic, frame):
    RGB_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
   
    result = holistic.process(RGB_frame)

    #right hand
    mp_drawing.draw_landmarks(frame, result.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
        mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
        mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
        )

    #Left Hand
    mp_drawing.draw_landmarks(frame, result.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
        mp_drawing.DrawingSpec(color=(12,22,76), thickness=2, circle_radius=4),
        mp_drawing.DrawingSpec(color=(12,44,250), thickness=2, circle_radius=2)
        )



options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='HandGesture\\gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)
with GestureRecognizer.create_from_options(options) as recognizer, mp_holistic.Holistic(min_detection_confidence = .5, min_tracking_confidence=.5) as holistic:
    
    cam = cv.VideoCapture(0)
    currentStateCount = 0
    previousState = ''
    while True:
        # Capture frame-by-frame
        ret, frame = cam.read()

        if not ret:
            print("error in retrieving frame")
            break
            
        getGesture(recognizer=recognizer, frame=frame)
        #printHandOutline(holisitic=holistic, frame=frame)


        if(globalResult is not None and len(globalResult.gestures) != 0):
            top_gesture = globalResult.gestures[0][0]
        else:
            top_gesture = None
        
        title = ''
        if top_gesture:
            title = f"{top_gesture.category_name} ({top_gesture.score:.2f})"
        
        if title != '' and previousState != title:
            #make sure it is the right option
            currentStateCount = currentStateCount + 1
            if(currentStateCount == 30):
                currentStateCount = 0
                previousState = title

        # display recognized gesture on screen
        org = (50, 50) 
        fontScale = 1
        color = (255, 0, 0) 
        thickness = 2
        image = cv.putText(frame, 'state: ' + previousState + '\n' + title, org, cv.FONT_HERSHEY_SIMPLEX ,  
                        fontScale, color, thickness, cv.LINE_AA) 

        cv.imshow('camera', image)
         
        if cv.waitKey(1) == ord('q'):
            break


    
cam.release()