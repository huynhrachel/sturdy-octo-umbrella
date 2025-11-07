# Proposal

## What will (likely) be the title of your project?

Collect Game

## In just a sentence or two, summarize your project. (E.g., "A website that lets you buy and sell stocks.")

A small desktop game built with Python’s Tkinter library where the player controls a red square to collect white dots within a limited time. The game keeps score, detects collisions, and displays win/lose messages.

## In a paragraph or more, detail your project. What will your software do? What features will it have? How will it be executed?

This project is a simple yet interactive Python game created using Tkinter. The program opens a 500×500 pixel window with a black background, where the player (a red square) can move using the arrow keys or WASD. White dots are randomly placed on the board, and the player’s goal is to collect all of them before the timer runs out. Each collected dot increases the score, and once all are gone, a “YOU WIN” message appears. If time runs out before all items are collected, a “GAME OVER” message is displayed.
The project demonstrates understanding of GUI programming, keyboard event handling, collision detection, and real-time updates in Python. It will be executed entirely using the Tkinter library, without external frameworks, making it portable and easy to run.

## If planning to combine 1051's final project with another course's final project, with which other course? And which aspect(s) of your proposed project would relate to 1051, and which aspect(s) would relate to the other course?

this project is designed solely for CIS 1051

## If planning to collaborate with 1 or 2 classmates for the final project, list their names, email addresses, and the names of their assigned TAs below.

I plan to complete this project individually.

## In the world of software, most everything takes longer to implement than you expect. And so it's not uncommon to accomplish less in a fixed amount of time than you hope.

### In a sentence (or list of features), define a GOOD outcome for your final project. I.e., what WILL you accomplish no matter what?

A working Tkinter window with a movable red player square.

Basic keyboard controls (arrow keys and WASD).

### In a sentence (or list of features), define a BETTER outcome for your final project. I.e., what do you THINK you can accomplish before the final project's deadline?

Add collectible white dots that disappear when touched.

A score counter that increases with each collected item.

### In a sentence (or list of features), define a BEST outcome for your final project. I.e., what do you HOPE to accomplish before the final project's deadline?

Add a countdown timer and “Game Over” message.

Include both win and lose conditions.

Add simple visual polish (colored layout, centered win message, smooth movement).

## In a paragraph or more, outline your next steps. What new skills will you need to acquire? What topics will you need to research? If working with one of two classmates, who will do what?

So far, I’ve completed around 65–70% of the project. I already built the main game window, movement system with arrow/WASD keys, score tracking, and item generation on the canvas. The player can move smoothly and interact with static objects. What’s left now is to add a limited-time feature (countdown timer) and implement collision checking properly so that the white dots disappear when the red square touches them. I also plan to improve the visuals to make the game more polished, such as better layout, color coordination, and smoother animations. In the process, I’ll learn more about how Tkinter’s after() function works for timing, how collision detection is handled within Canvas, and maybe how to package the game as a simple .exe file later on.
