import cv2
import mediapipe as mp
import time
import random
import menu
from sys import exit

class App():

    def __init__(self, width_menu, height_menu, list):
        self.exit = False
        cap = cv2.VideoCapture(0)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


        mpHands = mp.solutions.hands
        hands = mpHands.Hands(static_image_mode=False,
                            max_num_hands=2,
                            min_detection_confidence=0.5,
                            min_tracking_confidence=0.5)
        mpDraw = mp.solutions.drawing_utils

        pTime = 0
        cTime = 0

        word_list = list
        score = 0

        # QUIT MESSAGE
        quit_msg = "press esc to quit"


        GOAL = 28 # 28 months since we started dating
        word = random.choice(word_list)
        while True:
            success, img = cap.read()
            img = cv2.flip(img, 1) # laterally invert it
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)

            # Initialize red_square_pos and red_square_len/height if not defined
            red_square_height = 50
            if 'red_square_len' not in locals():
                red_square_len = len(word)*20
            if 'red_square_pos' not in locals():
                red_square_pos = (random.randint(50, width-red_square_len), random.randint(50, height-red_square_height))

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    for id, lm in enumerate(handLms.landmark):
                        h, w, c = img.shape # frame dimensions
                        cx, cy = int(lm.x * w), int(lm.y * h) # convert to device coordinates

                        cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED) # draw those landmarks

                        # Check if hand is close to the dynamic-sized rectangle
                        if (
                            red_square_pos[0] < cx < red_square_pos[0] + red_square_len
                            and red_square_pos[1] < cy < red_square_pos[1] + red_square_height
                        ):
                            # Hand is close, respawn dynamic-sized rectangle and update score
                            word = random.choice(word_list)
                            red_square_pos = (random.randint(50, width-red_square_len), random.randint(50, height-red_square_height))
                            score += 1
                            red_square_len = len(word)*20

                    mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # Display score
            if score < GOAL:
                score_txt = f"Score: {score}"
            else:
                score_txt = "28 months! and more"
                word = "We Made it!"
                red_square_len = len(word) * 20 


            # Draw dynamic-sized rectangle
            cv2.rectangle(
                img,
                (red_square_pos[0], red_square_pos[1]),
                (red_square_pos[0] + red_square_len, red_square_pos[1] + 50),
                (100,2,200),
                cv2.FILLED,
            )


            cv2.putText(
                img,
                score_txt,
                (10, 30),
                cv2.FONT_HERSHEY_PLAIN,
                2,
                (160,32,240),
                2,
            )

            # display the word:
            cv2.putText(img, word, 
                        (red_square_pos[0]+10,
                        int(red_square_pos[1]+red_square_height/2)),
                        cv2.FONT_HERSHEY_PLAIN,
                        2,
                        (255,255,255),
                        2,)

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (160,32,240), 2)

            # QUIT MESSAGE
            cv2.rectangle(img,(width//2-len(quit_msg)*10-20, height-40), (width//2+len(quit_msg)*10, height),(144,2,106),cv2.FILLED)
            cv2.putText(img, quit_msg, (width//2-len(quit_msg)*10, height-10), cv2.FONT_HERSHEY_PLAIN, 2, (227,158,152), 2)

            cv2.imshow("Image", img)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # 27 corresponds to the 'ESC' key
                break
        menu.App(width_menu, height_menu, list)
        
