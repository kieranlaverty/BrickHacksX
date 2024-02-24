import mediapipe as mp
import cv2

def opencam():
    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic

    #set the opencv to capture video
    capture = cv2.VideoCapture(0)

    with mp_holistic.Holistic(min_detection_confidence = .5, min_tracking_confidence=.5) as holistic:
        
        #take the video live
        while capture.isOpened():

            #frame is the camera frame
            ret, frame = capture.read()
            
            #change the color type to rgb for mediapipe 
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            #finding markers
            results = holistic.process(image)
            

            #change the color type to bgr for opencv 
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


            # Draw face landmarks
            mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
                mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                )
            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                )
            
            #show frame
            cv2.imshow("camera feed", image)

        capture.release()
        cv2.destroyAllWindows()


def main():
    opencam()





if __name__ == '__main__':
    main()