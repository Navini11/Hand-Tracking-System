import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
    # mode: Determines if the model is static or dynamic. Default is False (dynamic).
    # maxHands: Maximum number of hands to detect. Default is 2.
    # detectionCon: Minimum confidence for initial hand detection. Default is 0.5.
    # trackCon: Minimum confidence for hand tracking. Default is 0.5.
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True): 
    # Converts the image to RGB, processes it to find hand landmarks, and optionally draws them on the image.
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True,point=0):
    # Retrieves and optionally draws the positions of landmarks for a specified hand and landmark index.
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if (draw and id==point):
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList


def main():
#Captures video from the webcam, processes each frame to detect hands and landmarks, and displays the video with FPS.
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = cv2.flip(img,1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=True,point=1)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1) #1ms delay
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Check if 'q' key is pressed
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
