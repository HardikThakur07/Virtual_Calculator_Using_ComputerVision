import cv2
from cvzone.HandTrackingModule import HandDetector
import pyttsx3
import math

# ---------------- STARTING AUDIO ---------------- #
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

engine.say("Please wait! The virtual calculator is starting")
engine.runAndWait()


class CalculatorButton:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(
            img,
            self.pos,
            (self.pos[0] + self.width, self.pos[1] + self.height),
            (125, 125, 225),
            cv2.FILLED
        )

        cv2.rectangle(
            img,
            self.pos,
            (self.pos[0] + self.width, self.pos[1] + self.height),
            (50, 50, 50),
            3
        )

        cv2.putText(
            img,
            self.value,
            (self.pos[0] + 30, self.pos[1] + 65),
            cv2.FONT_HERSHEY_PLAIN,
            3,
            (50, 50, 50),
            3
        )

    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and \
           self.pos[1] < y < self.pos[1] + self.height:
            return True
        return False


# ---------------- BUTTON LAYOUT ---------------- #
buttons = [
    ['7', '8', '9', 'C'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '+'],
    ['0', '-', '/', '='],
    ['(', ')', '.', 'del']
]

buttonList = []

for x in range(4):
    for y in range(5):
        xpos = x * 100 + 700
        ypos = y * 100 + 150

        buttonList.append(
            CalculatorButton(
                (xpos, ypos),
                100,
                100,
                buttons[y][x]
            )
        )

# ---------------- VARIABLES ---------------- #
Equation = ''
Counter = 0

# ---------------- WEBCAM ---------------- #
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(3, 1280)
cap.set(4, 720)

# ---------------- HAND DETECTOR ---------------- #
detector = HandDetector(
    detectionCon=0.8,
    maxHands=1
)

# ---------------- MAIN LOOP ---------------- #
while True:

    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)

    # Detect Hands
    hands, img = detector.findHands(img)

    # Draw Buttons
    for button in buttonList:
        button.draw(img)

    # Draw Display
    cv2.rectangle(
        img,
        (700, 40),
        (1100, 120),
        (175, 125, 155),
        cv2.FILLED
    )

    cv2.rectangle(
        img,
        (700, 40),
        (1100, 120),
        (50, 50, 50),
        3
    )

    cv2.putText(
        img,
        Equation,
        (710, 95),
        cv2.FONT_HERSHEY_PLAIN,
        3,
        (0, 0, 0),
        3
    )

    cv2.putText(
        img,
        'VIRTUAL CALCULATOR -->',
        (50, 70),
        cv2.FONT_HERSHEY_PLAIN,
        3,
        (0, 0, 0),
        3
    )

    # ---------------- HAND INTERACTION ---------------- #
    if hands:

        lmList = hands[0]['lmList']

        # Get only x,y coordinates
        x, y = lmList[8][:2]

        p1 = lmList[8][:2]
        p2 = lmList[12][:2]

        # Distance between index and middle finger
        length, _, img = detector.findDistance(p1, p2, img)

        # Click Detection
        if length < 40 and Counter == 0:

            for i, button in enumerate(buttonList):

                if button.checkClick(x, y):

                    myValue = button.value

                    # Visual Click Effect
                    cv2.rectangle(
                        img,
                        button.pos,
                        (button.pos[0] + button.width,
                         button.pos[1] + button.height),
                        (255, 255, 255),
                        cv2.FILLED
                    )

                    cv2.putText(
                        img,
                        myValue,
                        (button.pos[0] + 30, button.pos[1] + 65),
                        cv2.FONT_HERSHEY_PLAIN,
                        3,
                        (0, 0, 0),
                        3
                    )

                    # Calculator Logic
                    if myValue == '=':

                        try:
                            Equation = str(eval(Equation))

                        except:
                            Equation = 'Error'

                    elif myValue == 'C':
                        Equation = ''

                    elif myValue == 'del':
                        Equation = Equation[:-1]

                    elif Equation == 'Error':
                        Equation = ''

                    else:
                        Equation += myValue

                    Counter = 1

    # ---------------- CLICK DELAY ---------------- #
    if Counter != 0:
        Counter += 1

        if Counter > 10:
            Counter = 0

    # ---------------- SHOW WINDOW ---------------- #
    cv2.imshow("Virtual Calculator", img)

    # Press Q to Exit
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()