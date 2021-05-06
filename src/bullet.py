import colorama
from colorama import Fore, Back, Style

# custom modules
from constants import Y0, ROWS


class Bullet:
    '''Bullets for Shooting Paddle'''

    def __init__(self, game, x, y=Y0-1):
        self.utils = game.utils
        self.game = game
        self.x = x
        self.y = y
        self.yv = -1
        self.xv = 0
        self._char = ' '
        self._color = Back.WHITE

    def move(self):
        self.y += self.yv
        if self.y <= 1:
            self.game.bullets.remove(self)

    def display(self):
        y = self.y
        x = self.x
        arr = self.game.board
        arr[y][x] = self._color + self._char
        #arr[y][x+1] = Style.RESET_ALL + arr[y][x+1]
        self.game.board = arr

    def brickCollision(self, brick):
        if self.y == brick.y + 1:
            if (self.x >= brick.x and self.x <= brick.x + brick.w - 1):
                brick.hit(self)
                self.game.bullets.remove(self)
