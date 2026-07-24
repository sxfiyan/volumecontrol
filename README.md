# Hand Gesture Volume Control 🖐️🔊

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Hands-orange.svg)](https://google.github.io/mediapipe/)
[![macOS AppleScript](https://img.shields.io/badge/macOS-AppleScript-black.svg)](https://developer.apple.com/)
[![Windows Pycaw](https://img.shields.io/badge/Windows-Pycaw-blueviolet.svg)](https://github.com/AndreMiras/pycaw)

An AI-powered computer vision application that enables touchless, gesture-based volume control using your computer's webcam. By tracking hand landmarks in real-time, the system measures the Euclidean distance between the thumb tip and index finger tip and seamlessly maps it to your operating system's audio volume.

---

## 📌 Features

- **Real-Time Hand Landmark Tracking**: Detects 21 hand keypoints at high FPS using Google MediaPipe Hands.
- **Precision Distance Mapping**: Measures thumb-to-index pinch distance and maps it smoothly to 0% - 100% volume level.
- **Jitter-Free Exponential Smoothing**: Uses Exponential Moving Average (EMA) filtering to prevent accidental volume fluctuations.
- **Cross-Platform Compatibility**: Supports macOS natively via AppleScript (`osascript`), Windows via `Pycaw` (COM API), and Linux via `amixer`.
- **Modern HUD Visual Overlay**: Live display featuring volume progress bar, numerical percentage, FPS counter, and gesture indicator line.
- **Zero-Install Web Demo**: Includes a browser-based live demo using MediaPipe JS and WebRTC for immediate testing in Chrome/Safari without local Python dependencies.

---

## 🏗️ System Architecture & Workflow

```
┌─────────────────┐       ┌──────────────────────┐       ┌──────────────────────┐
│  Webcam Stream  │ ────> │ MediaPipe Hand Model │ ────> │ Extract Landmarks    │
└─────────────────┘       └──────────────────────┘       │ (Thumb ID4, Index ID8)│
                                                         └──────────┬───────────┘
                                                                    │
┌─────────────────┐       ┌──────────────────────┐       ┌──────────▼───────────┐
│ System Volume   │ <──── │ EMA Smoothing Filter │ <──── │ Euclidean Distance   │
│ Adjustment      │       │ & Linear Interpolation│       │ Calculation (px)     │
└─────────────────┘       └──────────────────────┘       └──────────────────────┘
```

---

## 📐 Mathematical Formulation

### 1. Euclidean Distance
The distance $d$ between Thumb Tip ($x_1, y_1$) and Index Finger Tip ($x_2, y_2$) is calculated as:
$$d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$

### 2. Linear Interpolation Range Mapping
The pixel distance $d \in [d_{\min}, d_{\max}]$ (e.g., $25\text{px} \rightarrow 200\text{px}$) is mapped to volume percentage $V \in [0, 100]$:
$$V_{\text{raw}} = \text{interp}(d, [d_{\min}, d_{\max}], [0, 100])$$

### 3. Exponential Moving Average (EMA) Smoothing
To eliminate video frame noise and micro-hand tremors:
$$V_{\text{smooth}}^{(t)} = \alpha \cdot V_{\text{raw}}^{(t)} + (1 - \alpha) \cdot V_{\text{smooth}}^{(t-1)}$$
*(where $\alpha = 0.2$ provides responsive yet stable transitions).*

---

## 📂 Project Structure

```text
hand gesture/
├── main.py                  # Main entry application & HUD overlay loop
├── hand_tracking_module.py  # Modular MediaPipe HandDetector class
├── volume_control.py        # Cross-platform system volume abstraction
├── requirements.txt         # Package dependency specifications
├── web_demo/                # Interactive zero-install browser application
│   └── index.html           # WebRTC + MediaPipe JS + Web Audio demo
├── Project_Report.md        # Comprehensive technical report
├── Presentation.md          # PowerPoint presentation slide deck
├── presentation.html        # Interactive HTML presentation slides
└── video_script_and_demo.md # Video storyboard & demonstration guide
```

---

## 🚀 Quick Setup & Installation

### Option 1: Python Native Application

1. **Clone or navigate to project folder:**
   ```bash
   cd "/Users/rayan/Documents/hand guesture"
   ```

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note for macOS users:* Ensure Xcode Command Line Tools are enabled if prompted (`xcode-select --install`).

3. **Run the application:**
   ```bash
   python3 main.py
   ```

---

### Option 2: Zero-Install Browser Live Demo

Open `web_demo/index.html` in Chrome or Safari:
- Allows instant live camera gesture tracking via WebRTC.
- Includes a Web Audio sound synthesizer to test volume control live.
- Features a distance simulator slider for testing without a webcam.

---

## 🎮 Controls & Shortcuts

| Hotkey / Gesture | Action |
| :--- | :--- |
| **Pinch Fingers Together** | Lower volume towards 0% (Green highlight when pinched) |
| **Spread Fingers Apart** | Increase volume up to 100% |
| **`'p'` Key** | Pause / Resume volume adjustment |
| **`'q'` Key** | Quit application |

---

## 🧪 Testing & Troubleshooting

- **Camera permissions on macOS:** If the camera feed is blank, ensure Terminal / Python has Camera access under `System Settings > Privacy & Security > Camera`.
- **Lighting conditions:** Ensure adequate lighting so hand landmarks are detected clearly.
- **Custom distance tuning:** Adjust `min_dist` and `max_dist` in `main.py` if your camera resolution or distance from screen requires calibration.

---

## 📜 License & Acknowledgments

Developed as an open-source Computer Vision & HCI project using **OpenCV**, **Google MediaPipe**, and **AppleScript / Pycaw**.
