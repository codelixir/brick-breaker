import time
import random
import colorama
from colorama import Fore, Back, Style
from collections import deque

# custom modules
from constants import COLS, ROWS, Y0
from ball import Ball


class PowerUp:
    '''Class for Power Ups'''

    def __init__(self, game, x, y, xvel=0, yvel=1):
        self.x = x
        self.y = y
        self.xv = xvel
        self.yv = yvel
        self._icon = True
        self._char = ''
        self._color = Fore.RESET
        self.utils = game.utils
        self.game = game
        self._idx = -1

    def activate(self):
        self._starttime = time.time()

    def deactivate(self):
        pass

    def active(self):
        if (time.time() - self._starttime > self.game.powerTimes[self._idx]):
            self.deactivate()

    def display(self):
        if self._icon:
            y = self.y
            x = self.x
            w = len(self._char)
            arr = self.game.board
            for i in range(w):
                arr[y][x+i] = self._color + self._char[i]
            arr[y][x+w] = Style.RESET_ALL + arr[y][x+w]
            self.game.board = arr

    def move(self):
        if self._icon:
            if (self.yv < 1):
                if random.random() > 0.66:
                    self.yv += 1
            if (self.x + self.xv <= 0 or self.x + self.xv >= COLS-2):
                self.xv = -self.xv
            if (self.y + self.yv <= 0):
                self.yv = -self.yv
            if (self.y >= ROWS-2):
                self._icon = False
                self.game.powerUpIcons.remove(self)
            else:
                self.x += self.xv
                self.y += self.yv
        self.paddleAbsorb(self.game.pad)

    def paddleAbsorb(self, paddle):
        y = self.y
        x = self.x
        if (y == Y0-1 or y == Y0 or y == Y0+1):
            if (x >= paddle.x - paddle.width//2 - 1 and x <= paddle.x + paddle.width//2 + 1):
                self.game.powerUpIcons.remove(self)
                self.activate()
                self._icon = False


class Coin(PowerUp):
    def __init__(self, game, x, y, xvel=0, yvel=1):
        super().__init__(game, x, y, xvel, yvel)
        self._char = '$'
        self._color = Fore.YELLOW

    def activate(self):
        self.utils.score += 100


class OneUp(PowerUp):
    def __init__(self, game, x, y, xvel=0, yvel=1):
        super().__init__(game, x, y, xvel, yvel)
        self._char = '♥'
        self._color = Fore.GREEN

    def activate(self):
        if self.utils.lives < 3:
            self.utils.lives += 1


class MultiBall(PowerUp):
    def __init__(self, game, x, y, xvel=0, yvel=1):
        super().__init__(game, x, y, xvel, yvel)
        self._char = '∴'
        self._color = Fore.BLUE

    def activate(self):
        for b in self.game.balls[:]:
            b.split()


class ExpandPaddle(PowerUp):
    def __init__(self, game, x, y, xvel=0, yvel=1):
        super().__init__(game, x, y, xvel, yvel)
        self._char = '<>'
        self._color = Fore.GREEN
        self._idx = 0
        self._time = 15

    def activate(self):
        if not self.game.powerTimes[self._idx]:
            self.game.activePowers.append(self)
            self._starttime = time.time()
            self.game.pad.grow(4)
        self.game.powerTimes[self._idx] += self._time

    def deactivate(self):
        self.game.powerTimes[self._idx] = 0
        self.game.activePowers.remove(self)
        self.game.pad.shrink(4)


class ShrinkPaddle(PowerUp):
    def __init__(self, game, x, y, xvel=0, yvel=1):
        super().__init__(game, x, y, xvel, yvel)
        self._char = '><'
        self._color = Fore.RED
        self._idx = 1
        self._time = 10

    def activate(self):
        if not self.game.powerTimes[self._idx]:
            self.game.activePowers.append(self)
            self._starttime = time.time()
            self.game.pad.shrink(4)
        self.game.powerTimes[self._idx] += self._time

    def deactivate(self):
        self.game.powerTimes[self._idx] = 0
        self.game.activePowers.remove(self)
        self.game.pad.grow(4)


class FastBall(PowerUp):
    def __init__(self, game, x, y, xvel=0, yvel=1):
        super().__init__(game, x, y, xvel, yvel)
        self._char = 'ϟ'
        self._color = Fore.RED
        self._idx = 2
        self._time = 10

    def activate(self):
        if not self.game.powerTimes[self._idx]:
            self.game.activePowers.append(self)
            self._starttime = time.time()
            for b in self.game.balls:
                b.speedUp()
        self.game.powerTimes[self._idx] += self._time

    def deactivate(self):
        self.game.powerTimes[self._idx] = 0
        self.game.activePowers.remove(self)
        for b in self.game.balls:
            b.slowDown()


class ThruBall(PowerUp):
    def __init__(self, game, x, y, xvel=0, yvel=1):
        super().__init__(game, x, y, xvel, yvel)
        self._char = '⥮'
        self._color = Fore.CYAN
        self._idx = 3
        self._time = 15

    def activate(self):
        if not self.game.powerTimes[self._idx]:
            self.game.activePowers.append(self)
            self._starttime = time.time()
            for b in self.game.balls:
                b.setThru(True)
        self.game.powerTimes[self._idx] += self._time

    def deactivate(self):
        self.game.powerTimes[self._idx] = 0
        self.game.activePowers.remove(self)
        for b in self.game.balls:
            b.setThru(False)


class PaddleGrab(PowerUp):
    def __init__(self, game, x, y, xvel=0, yvel=1):
        super().__init__(game, x, y, xvel, yvel)
        self._char = '⩃'
        self._color = Fore.BLUE
        self._idx = 4
        self._time = 30

    def activate(self):
        if not self.game.powerTimes[self._idx]:
            self.game.activePowers.append(self)
            self._starttime = time.time()
            for b in self.game.balls:
                b.setGrab(True)
        self.game.powerTimes[self._idx] += self._time

    def deactivate(self):
        self.game.powerTimes[self._idx] = 0
        self.game.activePowers.remove(self)
        for b in self.game.balls:
            b.setGrab(False)


class PaddleShoot(PowerUp):
    def __init__(self, game, x, y, xvel=0, yvel=1):
        super().__init__(game, x, y, xvel, yvel)
        self._char = '↑'
        self._color = Fore.MAGENTA
        self._idx = 5
        self._time = 30

    def active(self):
        remtime = self.game.powerTimes[self._idx] - \
            (time.time() - self._starttime)
        self.utils.powtime = int(remtime)
        if (time.time() - self._starttime > self.game.powerTimes[self._idx]):
            self.game.powerTimes[self._idx] = 0
            self.deactivate()

    def activate(self):
        if not self.game.powerTimes[self._idx]:
            self.game.activePowers.append(self)
            self._starttime = time.time()
            self.game.pad.shoot()
        self.game.powerTimes[self._idx] += self._time

    def deactivate(self):
        self.game.powerTimes[self._idx] = 0
        self.game.pad.shoot(False)
        self.utils.powtime = 0
        self.game.activePowers.remove(self)


class FireBall(PowerUp):
    def __init__(self, game, x, y, xvel=0, yvel=1):
        super().__init__(game, x, y, xvel, yvel)
        self._char = '✸'
        self._color = Fore.YELLOW
        self._idx = 6
        self._time = 15

    def activate(self):
        if not self.game.powerTimes[self._idx]:
            self.game.activePowers.append(self)
            self._starttime = time.time()
            for b in self.game.balls:
                b.setFire(True)
        self.game.powerTimes[self._idx] += self._time

    def deactivate(self):
        self.game.powerTimes[self._idx] = 0
        self.game.activePowers.remove(self)
        for b in self.game.balls:
            b.setFire(False)


PowerList = [ExpandPaddle, ShrinkPaddle, FastBall, ThruBall,
             PaddleGrab, PaddleShoot, FireBall, MultiBall, OneUp, Coin, Coin, Coin]


def getPowerUp(brick, ball):
    idx = random.randint(0, 11)
    pu = PowerList[idx]
    brick.game.powerUpIcons.append(
        pu(brick.game, brick.x, brick.y, ball.xv, ball.yv))
