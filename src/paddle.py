import time
import colorama
from colorama import Fore, Back, Style

# custom modules
from constants import COLS, X0, Y0
from bullet import Bullet


class Paddle:
    """Class for Paddle object"""

    def __init__(self, game, width):
        self.utils = game.utils
        self.game = game
        self.width = width
        self.x = X0  # (x, y) are coordinates of the centre
        self.y = Y0
        self.v = 3
        self._color = Back.RED
        self._char = ' '
        self._shoot = False

    def reset(self):
        self.x = X0
        self.y = Y0

    def move(self, dirn=1):
        w = self.width//2
        x = self.x
        if (x+w >= COLS-2 and dirn == 1):
            return
        if (x-w <= 1 and dirn == -1):
            return
        self.x += self.v*dirn

    def display(self):
        y = self.y
        w = self.width//2
        x = self.x
        arr = self.game.board
        if (x - w <= 0):
            x = w
        elif (x + w >= COLS-1):
            x = COLS-1-w
        if self._shoot:
            color = Back.MAGENTA
        else:
            color = self._color
        for x in range(self.x - w, self.x + w):
            arr[y][x] = color + self._char
        arr[y][self.x + w] = Style.RESET_ALL + arr[y][self.x + w]
        self.game.board = arr

    def grow(self, amt=2):
        if self.width < 20:
            self.width += amt
        if (self.width//2 + self.x) >= COLS-1:
            self.x = COLS - self.width//2 - 1

    def shrink(self, amt):
        if self.width > 6:
            self.width -= amt

    def shoot(self, val=True):
        self._shoot = val

    def release(self):
        if self._shoot:
            timenow = time.time()-self.utils.time
            if (timenow - int(timenow) < 0.1) or (timenow - int(timenow) > 0.9):
                b1 = Bullet(self.game, self.x - self.width // 2)
                b2 = Bullet(self.game, self.x + self.width // 2)
                self.game.bullets.append(b1)
                self.game.bullets.append(b2)
