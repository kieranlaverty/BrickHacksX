import mediapipe as mp
import cv2 as cv
import time
import threading

#trivia
import json
import requests

API_URL = "https://opentdb.com/api.php?amount=10&difficulty=easy&type=boolean"


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
        #print('gesture recognition result: {}'.format(result.gestures))
        pass
    global globalResult
    globalResult = result

def getGesture(recognizer, frame):
    rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    thread = threading.Thread(target=recognizer.recognize_async, args=(rgb_frame, current_milli_time()))
    thread.start()
    thread.join()

    #print(globalResult)

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
    
    # state and game state variables
    currentGestureStateCount = 0
    #previousGestureState = ''
    currentGestureState = ''
    previousGameState = 'Main'
    currentGameState = 'Main'
    loadQuestions = True
    showMesh = True
    questionNumber = 0
    midQuestion = False
    correct_answers = 0

    #set up trivia variables
    response = requests.get(API_URL)
    data = json.loads(response.text)
    questions = data["results"]

    cam = cv.VideoCapture(0)
    
    while True:
        # Capture frame-by-frame
        ret, frame = cam.read()

        if not ret:
            print("error in retrieving frame")
            break
            
        getGesture(recognizer=recognizer, frame=frame)
        if showMesh:
            printHandOutline(holisitic=holistic, frame=frame)


        if(globalResult is not None and len(globalResult.gestures) != 0):
            top_gesture = globalResult.gestures[0][0]
        else:
            top_gesture = None
        
        title = ''
        if top_gesture:
            title = f"{top_gesture.category_name} ({top_gesture.score:.2f})"
        
        #get current Gesture
        if title != '' and currentGestureState != title:
            #make sure it is the right option
            currentGestureStateCount = currentGestureStateCount + 1
            if(currentGestureStateCount == 30):
                currentGestureStateCount = 0
                currentGestureState = title
                if 'Pointing_Up' in title:
                    showMesh = not showMesh
                if 'ILoveYou' in title:
                    currentGameState = 'play'
                if 'Victory' in title:
                    currentGameState = 'main'
                    loadQuestions = True
                    questionNumber = 0
                    midQuestion = False
                    correct_answers = 0

        #game logic
        if currentGameState == 'main' and loadQuestions == True:
            #load up the questions for the next game
            response = requests.get(API_URL)
            data = json.loads(response.text)
            questions = data["results"]
            print(questions)
            loadQuestions = False
            questionNumber = 0
            correct_answers = 0

        if(questionNumber == 10):
            #print high score
            continue

        if(currentGameState == 'play' and not midQuestion and questionNumber < 10):
            midQuestion = True
            loadQuestions = True
            # ask a question
            question = questions[questionNumber]
            print(question["question"])
            print("Options:")
            gestureChoices = {0: "thumbs-down", 1: "thumbs-up"}
            for i in range(len(question["incorrect_answers"])):
                print(f"({gestureChoices[i]}) {question['incorrect_answers'][i]}")

            #print(f"{len(question['incorrect_answers'])+1}. {question['correct_answer']}")
            questionNumber = questionNumber + 1

            # resset currentGameState
            pass

        if midQuestion:
            if 'Thumb_Up' in currentGestureState:
                user_answer = 2
                if user_answer == len(question["incorrect_answers"]) + 1:
                    print("Correct!")
                    correct_answers += 1
                else:
                    print("Incorrect.")
                midQuestion = False
                currentGestureState = ''
                currentGestureStateCount = -50 # to let state reset
            if 'Thumb_Down' in currentGestureState:
                user_answer = 1
                if user_answer == len(question["incorrect_answers"]) + 1:
                    print("Correct!")
                    correct_answers += 1
                else:
                    print("Incorrect.")
                midQuestion = False
                currentGestureState = ''
                currentGestureStateCount = -50 # to let state reset

        
        #flipping the camera feed
        frame = cv.flip(frame, 1)

        #added_image = cv2.addWeighted(background,0.4,overlay,0.1,0)
        # display recognized gesture on screen
        org = (50, 50) 
        fontScale = 1
        color = (255, 0, 0) 
        thickness = 2
        outText = 'game: ' + currentGameState + '    controlState:' + currentGestureState +  'current: ' + title
        image = cv.putText(frame, outText, org, cv.FONT_HERSHEY_SIMPLEX ,  
                        fontScale, color, thickness, cv.LINE_AA) 
        

        # display question on screen
        question = "What is thekkjkkkkkkkkkkkkkkxx wing span of a swallow?"

        #text placement
        org = (0, 450) 

        #setting text scaling
        for scale in reversed(range(0, 60, 1)):
            textSize = cv.getTextSize(question, fontFace=cv.FONT_HERSHEY_DUPLEX, fontScale=scale/10, thickness=1)
            new_width = textSize[0][0]
            if (new_width <= 500):
                scale = scale/10
                break

        fontScale = min(200,30)/(25/scale)

        #text color
        color = (255, 0, 0) 

        #thickness
        thickness = 2
        
        #overlay text
        image = cv.putText(frame, question, org, cv.FONT_HERSHEY_SIMPLEX ,  
                        fontScale, color, thickness, cv.LINE_AA)
        


        cv.imshow('camera', image)
         
        if cv.waitKey(1) == ord('q'):
            break


    
cam.release()