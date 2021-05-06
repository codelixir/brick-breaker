[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

This project uses the **colorama** python library to make ANSI escape character sequences. \
[Read the official colorama documentation here](https://pypi.org/project/colorama/).

This game was made as a part of the Design and Analysis of Software Systems course, Spring 2021.

---


# Big Brick Energy

A game similar to Brick Breaker, but runs on terminal because flash player is dead.

## Installation and running

1. If you don't have colorama installed, \
   `pip3 install -r requirements.txt`
2. To run the game, \
   `python3 main.py` \
   For best results, have your terminal window in full screen mode.

## Controls

- `w` to release the ball from the paddle
- `a` to move left
- `d` to move right
- `;` to quit the game

## Power Ups

- `$` Coin
- `♥` 1Up
- `∴` Multi-Ball
- `<>` Expand Paddle
- `><` Shrink Paddle
- `ϟ` Fast Ball
- `⥮` Thru-Ball
- `⩃` Paddle-Grab
- `↑` Shooting Paddle
- `✸` Fire Ball

## Features

### Inheritance

All power-ups are inherited from the `PowerUp ` class.

### Polymorphism

Functions such as `display`, `move`, etc are common for multiple objects.

### Encapsulation

Multiple classes and objects are used.

### Abstraction

Many functions such as `activate`, `move`, etc are abstracted.