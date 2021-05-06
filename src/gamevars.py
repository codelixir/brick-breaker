'''Game Variables'''
import time
from paddle import Paddle
from ball import Ball
from brick import Brick, Explosive, Rainbow


class Game():
    def __init__(self, utils):
        self.utils = utils
        self.run = True
        layout_1 = [Brick(self, 5, 7, 1), Brick(self, 15, 3, 2), Brick(self, 15, 5, 3), Explosive(self, 15, 4), Brick(
            self, 5, 4, -1), Brick(self, 35, 6, 2), Explosive(self, 35, 5), Brick(self, 35, 4, 1), Brick(self, 50, 4, -1), Brick(self, 50, 7, 1)]
        layout_2 = [Rainbow(self, 5, 8), Rainbow(self, 15, 4), Rainbow(self, 15, 6), Explosive(self, 15, 5), Brick(
            self, 5, 5, -1), Rainbow(self, 35, 7), Explosive(self, 35, 6), Rainbow(self, 35, 5), Brick(self, 50, 5, -1), Rainbow(self, 50, 8)]
        layout_3 = [Brick(self, 5, 7, 2), Brick(self, 15, 3, 3), Brick(self, 15, 5, 1), Explosive(self, 15, 4), Brick(self, 5, 4, -1), Brick(self, 35, 6, 3), Explosive(self, 35, 5), Brick(self, 25, 5, 3), Explosive(self, 25, 6),
                    Brick(self, 25, 7, 2), Brick(self, 35, 4, 1), Brick(self, 50, 4, -1), Brick(self, 50, 7, 1), Rainbow(self, 10, 9), Rainbow(self, 20, 10), Rainbow(self, 30, 9), Rainbow(self, 40, 10), Rainbow(self, 50, 9)]
        self.levels = [layout_1, layout_2, layout_3]
        self.pad = Paddle(self, 12)
        self.balls = [Ball(self)]
        self.bricks = self.levels[utils.level - 1]
        self.board = []
        self.powerUpIcons = []
        # grow, shrink, fast, thru, grab, shoot, fire
        self.powerTimes = [0, 0, 0, 0, 0, 0, 0]
        self.activePowers = []
        self.bullets = []

    def levelup(self):
        utils = self.utils
        if utils.level == 3:
            utils.score += utils.lives*100
            print("You win! Your final score is " + str(utils.score))
            self.run = False
        else:
            self.pad.reset()
            utils.play = False
            utils.time = time.time()
            for pu in self.activePowers[:]:
                pu.deactivate()
            self.balls = [Ball(self)]
            utils.level += 1
            self.bricks = self.levels[utils.level - 1]


class Utils():
    def __init__(self):
        self.score = 0
        self.level = 1
        self.lives = 3
        self.play = False
        self.falling = False
        self.time = time.time()
        self.powtime = 0
