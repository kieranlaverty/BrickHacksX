import mediapipe as mp
import cv2

def opencam():
    capture = cv2.VideoCapture(0)
    
    while capture.isOpened():
        ret, frame = capture.read()
        cv2.imshow("camera feed", frame)

        if cv2.waitKey(10) and (0xFF == ord('q')):
            break

    capture.release()
    cv2.destroyAllWindows()


def main():
    opencam()





if __name__ == '__main__':
    main()