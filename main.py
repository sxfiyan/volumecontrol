"""
Hand Gesture Volume Control - Main Application
------------------------------------------------
Tracks thumb & index finger distance in real time using webcam feed,
maps distance to system volume percentage, and renders live HUD overlay.
"""

import cv2
import numpy as np
import time
from hand_tracking_module import HandDetector
from volume_control import VolumeController


def run_application():
    # 1. Camera setup
    cam_width, cam_height = 640, 480
    cap = cv2.VideoCapture(0)
    cap.set(3, cam_width)
    cap.set(4, cam_height)

    if not cap.isOpened():
        print("[Error] Could not access webcam. Please check camera connection or permissions.")
        return

    # 2. Module initializations
    detector = HandDetector(detection_con=0.7, track_con=0.7, max_hands=1)
    vol_ctrl = VolumeController()

    # 3. Gesture Mapping Calibration Parameters
    min_dist = 25    # Distance in pixels corresponding to 0% volume
    max_dist = 200   # Distance in pixels corresponding to 100% volume
    vol_bar = 400    # Y-coordinate of volume bar display
    vol_per = vol_ctrl.get_volume()
    smooth_vol = float(vol_per)

    # 4. Loop & Smoothing variables
    p_time = 0
    alpha = 0.2     # Smoothing factor for Exponential Moving Average
    control_active = True
    print("\n=======================================================")
    print("  Hand Gesture Volume Control Started Successfully!")
    print("  Press 'q' to Quit application.")
    print("  Press 'p' to Pause / Resume Volume Adjustments.")
    print("=======================================================\n")

    while True:
        success, img = cap.read()
        if not success or img is None:
            print("[Warning] Blank frame received. Skipping...")
            time.sleep(0.01)
            continue

        # Flip horizontally for natural mirror feel
        img = cv2.flip(img, 1)

        # Detect hands
        img = detector.find_hands(img, draw=True)
        lm_list = detector.find_positions(img, draw=False)

        if len(lm_list) != 0:
            # Thumb tip: ID 4, Index tip: ID 8
            x1, y1 = lm_list[4][1], lm_list[4][2]
            x2, y2 = lm_list[8][1], lm_list[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            # Calculate distance
            length, img, _ = detector.find_distance(4, 8, img, draw=False)

            # Map distance to volume percentage (0 - 100) & volume bar height (400 - 150)
            raw_vol = np.interp(length, [min_dist, max_dist], [0, 100])
            vol_bar = np.interp(length, [min_dist, max_dist], [400, 150])

            # Apply Exponential Smoothing to prevent volume jittering
            smooth_vol = alpha * raw_vol + (1 - alpha) * smooth_vol
            vol_per = int(smooth_vol)

            # Update system volume if control is active
            if control_active:
                vol_ctrl.set_volume(vol_per)

            # --- Visual UI Overlay Elements ---
            # Line connecting Thumb & Index Finger
            line_color = (255, 0, 255) if length > min_dist + 10 else (0, 255, 0)
            cv2.line(img, (x1, y1), (x2, y2), line_color, 3)
            cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 8, (255, 0, 255), cv2.FILLED)

            # Highlight center point when pinched close
            if length < min_dist + 15:
                cv2.circle(img, (cx, cy), 12, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, (cx, cy), 16, (0, 255, 0), 2)
            else:
                cv2.circle(img, (cx, cy), 8, (0, 215, 255), cv2.FILLED)

            # Distance readout tag
            cv2.putText(img, f"{int(length)} px", (cx + 15, cy - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        # --- Draw HUD Glassmorphic Volume Bar ---
        # Outer Border
        cv2.rectangle(img, (40, 150), (75, 400), (255, 255, 255), 2)
        # Inner Filled Level
        cv2.rectangle(img, (40, int(vol_bar)), (75, 400), (0, 200, 255), cv2.FILLED)
        # Volume Percentage Badge
        cv2.putText(img, f'{vol_per}%', (35, 435), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 200, 255), 2)

        # --- Draw Top Bar Details (FPS & Control Status) ---
        c_time = time.time()
        fps = 1 / (c_time - p_time) if (c_time - p_time) > 0 else 0
        p_time = c_time

        # FPS badge
        cv2.rectangle(img, (15, 15), (150, 50), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, f'FPS: {int(fps)}', (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 128), 2)

        # Status badge
        status_text = "ACTIVE" if control_active else "PAUSED [P]"
        status_color = (0, 255, 0) if control_active else (0, 0, 255)
        cv2.putText(img, f'Status: {status_text}', (cam_width - 230, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, status_color, 2)

        # Show frame in window
        cv2.imshow("Hand Gesture Volume Control", img)

        # Keyboard interaction handler
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("[Info] Exiting Hand Gesture Volume Control...")
            break
        elif key == ord('p'):
            control_active = not control_active
            state = "Resumed" if control_active else "Paused"
            print(f"[Info] Volume Control {state}.")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_application()
