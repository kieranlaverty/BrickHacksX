import threading

import cv2 as cv

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2
from collections import deque
import math

base_options = python.BaseOptions(model_asset_path='HandGesture\\gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)


def gest(frame):
        
        
    rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    recognition_result = recognizer.recognize(rgb_frame)

    try:
        top_gesture = recognition_result.gestures[0][0]
    except IndexError:

        top_gesture = None

    hand_landmarks = recognition_result.hand_landmarks

    title = None
    if top_gesture:
        title = f"{top_gesture.category_name} ({top_gesture.score:.2f})"
        #print(title)
    return title

def pose():
   mp_hands = mp.solutions.hands
   hand = mp_hands.Hands()

   mp_holistic = mp.solutions.holistic

   mp_drawing = mp.solutions.drawing_utils

   cam = cv.VideoCapture(0)

   if not cam.isOpened():
      print("error opening camera")
      exit()
   
   previousState = None
   
   state = None
   with mp_holistic.Holistic(min_detection_confidence = .5, min_tracking_confidence=.5) as holistic:
      while True:
         
         # Capture frame-by-frame
         ret, frame = cam.read()
         if not ret:
            print("error in retrieving frame")
            break
         
         currentGesture = gest(frame)

         if currentGesture != None and currentGesture != previousState:
            previousState = state
            state = currentGesture
         print(state)



         #scaled the image by 2
         height, width = frame.shape[:2]
         frame = cv.resize(frame,(math.floor(1.5*width), math.floor(1.5*height)), interpolation = cv.INTER_CUBIC)
         
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
         if state is "Closed_Fist ":
            mp_drawing.draw_landmarks(frame, result.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
                mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                )
         
        #  #poses
        #  mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
        #        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
        #        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
        #        )

         

         img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        #  if not (result.right_hand_landmarks == None):
        #     x = result.right_hand_landmarks.landmark[9].x
        #     y = result.right_hand_landmarks.landmark[9].y
        #     if x > .50:
        #        print("right")
        #     else:
        #        print("no")
            
        #  if not (result.right_hand_landmarks == None):
        #     x = result.right_hand_landmarks.landmark[9].x
        #     y = result.right_hand_landmarks.landmark[9].y
        #     if x > .50:
        #        print("right")
        #     else:
        #        print("no")
         
         
         

         cv.imshow('frame', cv.flip(frame, 1))


         
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

