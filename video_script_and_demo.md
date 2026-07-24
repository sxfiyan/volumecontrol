# Demonstration Video Script & Testing Protocol 🎬🖐️

## Project Name: Hand Gesture Volume Control

This document provides a step-by-step storyboard, video recording script, voiceover narration transcript, and testing protocol to produce the demonstration video for the project.

---

## 📋 Video Overview

- **Target Video Duration:** 2 Minutes (120 Seconds)
- **Resolution:** 1080p Full HD (1920x1080) @ 60 FPS
- **Audio:** Clear voiceover commentary + system audio tone test

---

## 🎬 Storyboard & Scene Breakdown

| Scene | Duration | Visual Display | Voiceover Script / Narration |
| :--- | :--- | :--- | :--- |
| **Scene 1: Title & Introduction** | 0:00 - 0:20 | Title screen with slide deck or webcam window. Presenter holding hand up in frame. | *"Welcome to the Hand Gesture Volume Control demonstration. In this project, we demonstrate a touchless computer vision application that allows users to adjust system audio volume using simple hand gestures captured via webcam."* |
| **Scene 2: Architecture & Setup** | 0:20 - 0:45 | Brief display of `main.py` code window + `hand_tracking_module.py`. Shows MediaPipe landmark skeleton. | *"Built with Python, OpenCV, and Google MediaPipe, the system tracks 21 hand landmarks in real time. Specifically, we extract the coordinates of the thumb tip (Landmark 4) and index finger tip (Landmark 8)."* |
| **Scene 3: Live Gesture Control Demo** | 0:45 - 1:25 | Fullscreen camera window showing live HUD overlay. Presenter pinches fingers close to lower volume to 0%, then spreads fingers wide to 100%. | *"As I pinch my thumb and index finger close together, the Euclidean distance decreases, and system volume drops towards zero percent. Notice the green highlight indicator when pinched. As I move my fingers apart, the volume bar smoothly increases to 100% without stutter or jitter thanks to our exponential smoothing algorithm."* |
| **Scene 4: System Integration & Features** | 1:25 - 1:45 | Presenter presses `'p'` on keyboard to pause volume adjustment, then `'p'` again to resume. Screen shows OS volume slider changing in system menu. | *"The application interacts directly with macOS via native AppleScript and Windows via Pycaw. We can pause or resume gesture tracking at any time by pressing 'P' on the keyboard."* |
| **Scene 5: Conclusion & Web Demo** | 1:45 - 2:00 | Quick glimpse of `web_demo/index.html` browser demo and closing slide. | *"In addition to native desktop execution, we also built a zero-install browser demo using WebRTC. Thank you for watching!"* |

---

## 🧪 Demonstration Testing Protocol

Follow these steps when recording the demo video or presenting live:

1. **Environment Setup:**
   - Position webcam at eye level in a well-lit room.
   - Ensure background is clean with minimal background clutter.

2. **Launch Application:**
   - **Option A (Python Application):** Run `python3 main.py` in Terminal.
   - **Option B (Browser Live Demo):** Open `web_demo/index.html` in Chrome or Safari.

3. **Execution Steps:**
   - Start with hand outside frame $\rightarrow$ Confirm status reads "Hand Not Detected".
   - Bring hand into view $\rightarrow$ Landmark skeleton overlays cleanly on hand.
   - Pinch thumb & index finger to minimum distance ($< 25\text{px}$) $\rightarrow$ Confirm volume reads 0% and green indicator glows.
   - Expand thumb & index finger apart ($> 180\text{px}$) $\rightarrow$ Confirm volume reads 100% and bar fills completely.
   - Press `'p'` $\rightarrow$ Confirm status changes to "PAUSED".
   - Press `'q'` $\rightarrow$ Cleanly exit application.
