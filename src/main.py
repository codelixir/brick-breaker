import colorama
import sys
import os
import math
import time
import copy
import time
from colorama import Fore, Back, Style

# custom modules
from constants import ROWS, COLS, T
from gamevars import Utils, Game
from input import get_input
from paddle import Paddle
from ball import Ball
from brick import Brick, winCondition
from power import Coin, OneUp
from sound import play_sound

colorama.init()

# initialising the board
blank_board = []
for i in range(ROWS):
    row = [' ']*COLS
    row.append('\n')
    blank_board.append(row)

# game
utils = Utils()
game = Game(utils)

while game.run:
    key = get_input()
    game.board = copy.deepcopy(blank_board)

    print("\033[H\033[J", end="")

    # Display Game Objects
    game.pad.display()
    for br in game.bricks:
        br.display()
    for ball in game.balls:
        ball.display()
    for pu in game.powerUpIcons:
        pu.display()
    for bu in game.bullets:
        bu.display()

    #board = ''.join(game.board)

    # Display Game Info
    timenow = int(time.time()-utils.time)
    levelcard = Back.LIGHTBLACK_EX + "\tLEVEL: " + \
        str(utils.level) + "\t\t\t\t\t" + Style.RESET_ALL
    scorecard = Back.LIGHTBLACK_EX + "\tSCORE: " + \
        str(utils.score) + "\t\t\t\t\t" + Style.RESET_ALL
    lifecard = Back.LIGHTBLACK_EX + "\tLIVES: " + \
        '♥'*utils.lives + '♡'*(3-utils.lives) + "\t\t\t\t\t" + Style.RESET_ALL
    timecard = Back.LIGHTBLACK_EX + "\tTIME : " + str(timenow//60) + \
        ':' + str(timenow % 60).zfill(2) + "\t\t\t\t\t" + Style.RESET_ALL
    powercard = Back.LIGHTBLACK_EX + "\tLASER: " + str(utils.powtime//60) + \
        ':' + str(utils.powtime % 60).zfill(2) + "\t\t\t\t\t" + Style.RESET_ALL

    # print(board)
    for row in game.board:
        for c in row:
            print(c, end='')
    print(levelcard, scorecard, lifecard, timecard, powercard, sep='\n')

    if not utils.lives:
        print("GAME OVER")
        play_sound()
        game.run = False
    if winCondition(game.bricks):
        play_sound()
        game.levelup()

    # Move/Update Stuff
    if timenow > 60:
        utils.falling = True
    if utils.play:
        for ball in game.balls[:]:
            ball.move()
            ball.paddleCollision()
            for br in game.bricks[:]:
                ball.brickCollision(br)
            if ball.dead():
                play_sound()
                game.balls.remove(ball)
        game.pad.release()
    for pu in game.powerUpIcons[:]:
        pu.move()
    for pu in game.activePowers[:]:
        pu.active()
    for bu in game.bullets[:]:
        bu.move()
        for br in game.bricks[:]:
            bu.brickCollision(br)
    for br in game.bricks[:]:
        if br.destroyed():
            game.bricks.remove(br)
            utils.score += 100
    if not game.balls:
        game.pad.reset()
        utils.lives -= 1
        utils.play = False
        for pu in game.activePowers[:]:
            pu.deactivate()
        game.balls = [Ball(game)]

    if (key != None):
        time.sleep(T)

    if (key == ";"):
        play_sound()
        game.run = False
    elif (key == "w"):
        utils.play = True
    elif (key == "d"):
        game.pad.move()
        if not utils.play:
            for b in game.balls:
                b.x = game.pad.x
    elif (key == "a"):
        game.pad.move(-1)
        if not utils.play:
            for b in game.balls:
                b.x = game.pad.x
    elif (key == "."):
        play_sound()
        game.levelup()

    time.sleep(T)
