"""
Hand Tracking Module using OpenCV and MediaPipe
------------------------------------------------
Provides modular reusable HandDetector class for detecting hands,
extracting landmark positions, and measuring distances between landmarks.
"""

import cv2
import mediapipe as mp
import math
import time


class HandDetector:
    """
    Modular Hand Detector using MediaPipe Hands solution.
    """
    def __init__(self, mode=False, max_hands=1, detection_con=0.7, track_con=0.7):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        # MediaPipe initialization
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=float(self.detection_con),
            min_tracking_confidence=float(self.track_con)
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def find_hands(self, img, draw=True):
        """
        Processes image frame and draws hand landmarks if requested.
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks and draw:
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    img,
                    hand_lms,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_draw.DrawingSpec(color=(0, 255, 128), thickness=2, circle_radius=3),
                    self.mp_draw.DrawingSpec(color=(255, 200, 0), thickness=2, circle_radius=2)
                )
        return img

    def find_positions(self, img, hand_no=0, draw=True):
        """
        Returns list of landmark coordinates: [id, x, y] for a specific hand.
        """
        lm_list = []
        if self.results and self.results.multi_hand_landmarks:
            if hand_no < len(self.results.multi_hand_landmarks):
                my_hand = self.results.multi_hand_landmarks[hand_no]
                h, w, c = img.shape
                for id, lm in enumerate(my_hand.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        return lm_list

    def find_distance(self, p1, p2, img, draw=True, r=10, t=3):
        """
        Calculates Euclidean distance between landmark indices p1 and p2.
        Draws line and midpoint indicator on image.
        Returns: (distance, img, line_info [x1, y1, x2, y2, cx, cy])
        """
        lm_list = self.find_positions(img, draw=False)
        if len(lm_list) <= max(p1, p2):
            return 0, img, [0, 0, 0, 0, 0, 0]

        x1, y1 = lm_list[p1][1], lm_list[p1][2]
        x2, y2 = lm_list[p2][1], lm_list[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            # Draw line between landmarks
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            # Draw circles at endpoints
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            # Center circle
            cv2.circle(img, (cx, cy), r, (0, 255, 0), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]


def main():
    """Sample stand-alone test runner for HandDetector."""
    cap = cv2.VideoCapture(0)
    p_time = 0
    detector = HandDetector()

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture frame from camera.")
            break

        img = detector.find_hands(img)
        lm_list = detector.find_positions(img)
        if len(lm_list) != 0:
            print(f"Thumb Tip (ID 4): {lm_list[4]}, Index Tip (ID 8): {lm_list[8]}")

        c_time = time.time()
        fps = 1 / (c_time - p_time) if (c_time - p_time) > 0 else 0
        p_time = c_time

        cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.imshow("Hand Tracking Test", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
