# Project: Real-Time Ping Pong Game (Enhanced Edition)

This is an enhanced version of the base ping pong game built with Pygame, focusing on clean state management, robust collisions, replay options, and event-based audio. 

---

## What’s Provided

A working game skeleton with player and AI paddles, ball movement, score display, and an organized game loop ready for extension. 

---

## What We Implemented

- Refined paddle collisions using a swept check with the previous x-position to prevent high-speed tunneling and repositioning the ball just outside the paddle on impact.   
- Clear state machine: replay → playing → game_over, freezing gameplay at game over while showing the winner until the player acts.   
- Replay menu with Best of 3/5/7 mapped to first-to 2/3/4 and full resets of scores, ball, and paddles for each new match.   
- Event-based sounds for paddle hits, wall bounces, and scoring with safe fallbacks when audio devices or files are unavailable.   
- Simplified entry point so the engine owns the main loop and timing, removing a previous double-loop.   
- Dual controls (Arrow keys and W/S) with smooth AI tracking aligned to the expected behavior. 

---

## Vibecoding Q&A

See questions.md for the vibecoding prompts, analyses, and resolutions completed as part of this exercise. 

---

## Requirements

- Listed in requirements.txt at the project root. 

---

## Setup

Install dependencies and run the game from the project root. 
pip install -r requirements.txt
python main.py


---

## Controls

- Player: Up/Down Arrow or W/S to move the paddle.   
- AI: Smooth auto-tracking of the ball.   
- HUD: Scores render at the top; a center line divides the field. 

---

## Audio

- Sounds trigger on events only: paddle hit, wall bounce, and scoring.   
- If audio is unavailable or files are missing, the game runs silently via safe fallbacks. 

---

## Game Modes

- Choose Best of 3/5/7 on the replay menu; targets are first-to 2/3/4 respectively.   
- Press ESC from the replay menu to exit cleanly. 

---

## Project Structure

Ensure this layout so imports resolve correctly. 
```
pygame-pingpong/
├── main.py
├── requirements.txt
├── game/
│ ├── game_engine.py
│ ├── paddle.py
│ └── ball.py
└── README.md
```
