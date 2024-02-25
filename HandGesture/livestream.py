import mediapipe as mp
import cv2 as cv
import time
import threading
import asyncio

def current_milli_time():
    return round(time.time() * 1000)


BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a gesture recognizer instance with the live stream mode:
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    if result is not None:
        print('gesture recognition result: {}'.format(result.gestures))
    return result

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='HandGesture\\gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)
with GestureRecognizer.create_from_options(options) as recognizer:
    
    cam = cv.VideoCapture(0)
    i = 0
    while True:
        # Capture frame-by-frame
        ret, frame = cam.read()

        if not ret:
            print("error in retrieving frame")
            break
            
            
        rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        #asyncio.run(recognizer.recognize_async(rgb_frame, current_milli_time()))


        thread = threading.Thread(target=recognizer.recognize_async, args=(rgb_frame, current_milli_time()))
        thread.start()

    # Continue with other tasks while processing is happening asynchronously

    # Wait for the asynchronous processing to finish
        thread.join()


        # try:
        #     top_gesture = recognition_result.gestures[0][0]
        # except IndexError:

        #     top_gesture = None

        # hand_landmarks = recognition_result.hand_landmarks

        # if top_gesture:
        #     title = f"{top_gesture.category_name} ({top_gesture.score:.2f})"
        #     print(title)
        #cv.imshow('frame', frame)

        cv.imshow('frame', frame)
         
        if cv.waitKey(1) == ord('q'):
            break


    
cam.release()