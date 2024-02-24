import cv2 as cv
import mediapipe as mp

mp_hands = mp.solutions.hands
hand = mp_hands.Hands()

mp_drawing = mp.solutions.drawing_utils

cam = cv.VideoCapture(0)
#cc = cv.VideoWriter_fourcc(*'XVID')
#file = cv.VideoWriter('output.avi', cc, 15.0, (640, 480))

if not cam.isOpened():
   print("error opening camera")
   exit()
while True:
   # Capture frame-by-frame
   ret, frame = cam.read()
   # if frame is read correctly ret is True
   if not ret:
      print("error in retrieving frame")
      break
   
   RGB_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
   result = hand.process(RGB_frame)
   if result.multi_hand_landmarks:
      for hand_landmarks in result.multi_hand_landmarks:
         mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
   
   img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
   cv.imshow('frame', img)
   #file.write(img)

   
   if cv.waitKey(1) == ord('q'):
      break

cam.release()
#file.release()
cv.destroyAllWindows()
