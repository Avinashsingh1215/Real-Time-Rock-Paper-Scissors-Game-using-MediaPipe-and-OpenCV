# 🖐️ Real-Time Rock Paper Scissors Game using MediaPipe and OpenCV

A fun and interactive real-time **Rock-Paper-Scissors** game that uses **MediaPipe Hand Tracking** and **OpenCV** to recognize hand gestures through a webcam and determine game outcomes against the computer.

---

## 🎯 Features

- 🔍 Real-time **hand gesture recognition** using MediaPipe
- 🧠 Smart classification of hand poses: Rock ✊, Paper ✋, Scissors ✌️
- 🤖 Random move generation by the computer
- 🗣️ **Voice feedback** using `pyttsx3` for each round
- 📊 Score tracking for Player vs Computer
- 🎨 Color-coded hand landmarks and gesture icons for enhanced UX
- 🎮 Easy-to-use and fast game loop with responsive performance

---

## 🛠️ Technologies Used

- **Python**
- **MediaPipe** (Hand Tracking)
- **OpenCV** (Image processing and webcam feed)
- **Pyttsx3** (Text-to-speech)
- **NumPy**, **Random**

---

## 📺 Demo

Watch the game in action!  
*Inside the Files Section there is a demo video present click on that to see the working of this project *

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/Avinashsingh1215/real-time-rock-paper-scissors.git
cd real-time-rock-paper-scissors
```

2. Install Dependencies
   
Make sure you have Python 3 installed.
```bash

pip install -r requirements.txt
```
If requirements.txt is not available, install manually:

```bash
pip install opencv-python mediapipe pyttsx3 numpy
```
3. Run the Game
```bash
python rps_game.py
```

## 🧠 How It Works

**MediaPipe tracks hand landmarks and determines if the hand gesture matches a predefined Rock, Paper, or Scissors pose**.

**The computer randomly picks a move**.

**Results are displayed on screen with visual feedback, score is updated, and audio feedback announces the winner of each round**.

## 🎓 Learning Outcome

Hands-on experience with real-time computer vision

Integration of gesture recognition in interactive applications

Use of speech synthesis and UX design in games

Deep understanding of MediaPipe’s Hand Tracking module


