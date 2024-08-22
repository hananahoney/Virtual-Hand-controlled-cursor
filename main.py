import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
cursor_y = 0
# thumb_y = 0
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    img_height, img_width, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb)
    hands = output.multi_hand_landmarks
    # print(hands)
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand, mp.solutions.holistic.HAND_CONNECTIONS)
            landmarks = hand.landmark
            if landmarks:
                for id, landmark in enumerate(landmarks):
                    x = int( landmark.x * img_width )
                    y = int( landmark.y * img_height )
                    if id == 8:
                        cv2.circle(frame, center=(x,y), radius=10, color=(0,255,255))
                        cursor_x = screen_width/img_width * x
                        cursor_y = screen_height / img_height * y
                        pyautogui.moveTo(cursor_x, cursor_y)

                    if id == 4:
                        cv2.circle(frame, center=(x,y), radius=10, color=(0,255,255))
                        thumb_x = screen_width / img_width * x
                        thumb_y = screen_height / img_height * y

                        if abs(thumb_y - cursor_y) < 25:
                            pyautogui.click()
                            pyautogui.sleep(1)

    cv2.imshow("Virtual Mouse", frame)
    cv2.waitKey(1)