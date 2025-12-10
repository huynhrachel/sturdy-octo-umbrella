# preposal

see preposal.md

# 🐾 Collect Game – Pygame Project

A small and fun collect-the-items game built with **Python + Pygame**.
You play as a little cat running around the map, collecting items while trying not to get caught by the enemy.
It’s a simple project, but it helped me practice game loops, movement mechanics, collision detection, and using assets in Pygame.

---

## 🎮 Gameplay Overview

* Move using **arrow keys**
* Collect items that spawn at random positions
* Gain points every time you pick one up
* Avoid the enemy chasing you
* Reach the required score → **You win**
* Get hit by the enemy → **Game over**

The game is short, simple, and easy to tweak if you want to add more features later.

---

## ✨ Features

* Player movement using keyboard input
* Random item spawning
* Enemy movement + collision logic
* Score system
* Win / Lose screens
* Image sprites for player, item, and enemy
* Sound effects for collecting, getting hit, winning, and losing (if audio files are included)

---

## 📁 Project Structure

```
collect_game/
│
├── game.py                 # Main game file
│
└── assets/
    ├── player.png
    ├── enemy.png
    ├── item.png
    └── sounds/
        ├── meow.wav
        ├── hit.wav
        ├── win.wav
        └── lose.wav
```

Make sure the assets folder matches the paths used in your code.

---

## ▶️ How to Run the Game

1. Install Pygame

```
pip install pygame
```

2. Keep all images and sound files inside the `assets/` folder.

3. Run the game

```
python game.py
```

---

## 🧠 What I Learned

* How the Pygame loop works
* Handling keyboard input
* Loading and rendering sprites
* Detecting collisions
* Switching game states (playing → win/lose)
* Using mixer for sound effects
* Randomizing object positions

This project helped me understand the basics of 2D games and how to structure simple gameplay logic.

---

## 🚀 Future Improvements

* Add animation frames for walking
* Better enemy AI (pathfinding or chasing logic)
* Power-ups, levels, or increasing difficulty
* Background music
* Menu screen + pause option
* Replace rectangles with pixel-perfect collision

