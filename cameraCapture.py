import numpy as np
import cv2 as cv
import mediapipe as mp


def main():
   red_img  = np.full((682,512,3), (0,0,255), np.uint8)
   mp_hands = mp.solutions.hands
   hand = mp_hands.Hands()

   mp_holistic = mp.solutions.holistic

   mp_drawing = mp.solutions.drawing_utils

   cam = cv.VideoCapture(0)
   #cc = cv.VideoWriter_fourcc(*'XVID')
   #file = cv.VideoWriter('output.avi', cc, 15.0, (640, 480))

   if not cam.isOpened():
      print("error opening camera")
      exit()
   
   
   with mp_holistic.Holistic(min_detection_confidence = .5, min_tracking_confidence=.5) as holistic:
      while True:
         
         # Capture frame-by-frame
         ret, frame = cam.read()

         #scaled the image by 2
         height, width = frame.shape[:2]
         frame = cv.resize(frame,(2*width, 2*height), interpolation = cv.INTER_CUBIC)
         
         # if frame is read correctly ret is True
         if not ret:
            print("error in retrieving frame")
            break
         
         RGB_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
         result = hand.process(RGB_frame)
         """if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
               mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
               mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)"""
         
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
         
         #right hand index finger tip
         #x = result.right_hand_landmarks[].x 
         #y = result.right_hand_landmarks[].y

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
         #file.write(img)

         
         if cv.waitKey(1) == ord('q'):
            break

   cam.release()
   #file.release()
   cv.destroyAllWindows()




if __name__ == "__main__":
   main()
