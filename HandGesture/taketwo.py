import threading
import time
import cv2 as cv

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2

base_options = python.BaseOptions(model_asset_path='HandGesture\\gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

def current_milli_time():
    return round(time.time() * 1000)

def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    if result is not None:
        print('gesture recognition result: {}'.format(result.gestures))
    return result




def gest(frame):
   options = GestureRecognizerOptions(
   base_options=BaseOptions(model_asset_path='HandGesture\\gesture_recognizer.task'),
   running_mode=VisionRunningMode.LIVE_STREAM,
   result_callback=print_result) 
   recognizer = vision.GestureRecognizer.create_from_options(options)
   with GestureRecognizer.create_from_options(options) as recognizer:
    
                  
      rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

      #asyncio.run(recognizer.recognize_async(rgb_frame, current_milli_time()))


      thread = threading.Thread(target=recognizer.recognize_async, args=(rgb_frame, current_milli_time()))
      thread.start()

      # Continue with other tasks while processing is happening asynchronously

      # Wait for the asynchronous processing to finish
      thread.join()



def pose():
   mp_hands = mp.solutions.hands
   hand = mp_hands.Hands()

   mp_holistic = mp.solutions.holistic

   mp_drawing = mp.solutions.drawing_utils

   cam = cv.VideoCapture(0)

   if not cam.isOpened():
      print("error opening camera")
      exit()
   
   
   with mp_holistic.Holistic(min_detection_confidence = .5, min_tracking_confidence=.5) as holistic:

      while True:
         
         # Capture frame-by-frame
         ret, frame = cam.read()
         gest(frame)
         #scaled the image by 2
         height, width = frame.shape[:2]
         frame = cv.resize(frame,(2*width, 2*height), interpolation = cv.INTER_CUBIC)
         
         # if frame is read correctly ret is True
         if not ret:
            print("error in retrieving frame")
            break
         
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

         #faces
         mp_drawing.draw_landmarks(frame, result.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
               mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
               mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
               )
         
         #poses
         mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
               mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
               mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
               )
         

         img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

         if not (result.right_hand_landmarks == None):
            x = result.right_hand_landmarks.landmark[9].x
            y = result.right_hand_landmarks.landmark[9].y
            if x > .50:
               print("right")
            else:
               print("no")
            
         if not (result.right_hand_landmarks == None):
            x = result.right_hand_landmarks.landmark[9].x
            y = result.right_hand_landmarks.landmark[9].y
            if x > .50:
               print("right")
            else:
               print("no")
         
         
         

         cv.imshow('frame', img)


         
         if cv.waitKey(1) == ord('q'):
            break

   cam.release()
   #file.release()
   cv.destroyAllWindows()



def main():
    pose()
    """ t1 = threading.Thread(pose())
    t2 = threading.Thread(gest())

    t1.start()
    t2.start()

    t1.join()
    t2.join() """






if __name__ == "__main__":
   main()

