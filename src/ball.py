import colorama
from colorama import Fore, Back, Style

# custom modules
from constants import COLS, X0, Y0, ROWS


class Ball:
    '''Class for Ball object'''

    def __init__(self, game, x=X0, y=Y0-1, xvel=1, yvel=-1, thru=False, fire=False):
        self.utils = game.utils
        self.game = game
        self.x = x
        self.y = y
        self.xv = xvel
        self.yv = yvel
        self._char = '⬤'
        self._color = Fore.WHITE
        self._thru = thru
        self._fire = fire
        self._grab = False

    def move(self):
        if (self.x + self.xv <= 0 or self.x + self.xv >= COLS-2):
            self.xv = -self.xv
        if (self.y + self.yv <= 0 or self.y + self.yv >= ROWS-1):
            self.yv = -self.yv
        self.x += self.xv
        self.y += self.yv

    def display(self):
        y = self.y
        x = self.x
        arr = self.game.board
        if self._fire:
            ch = '✪'
            col = Fore.RED
        elif self._thru:
            ch = '✪'
            col = Fore.CYAN
        else:
            ch = self._char
            col = self._color
        arr[y][x] = col + ch
        arr[y][x+1] = Style.RESET_ALL + arr[y][x+1]
        self.game.board = arr

    def paddleCollision(self):
        y = self.y + self.yv
        x = self.x
        X = self.game.pad.x
        W = self.game.pad.width
        if (y >= Y0):
            if (x >= X - W//2 and x <= X + W//2):
                self.yv = -self.yv
                if self.utils.falling:
                    for b in self.game.bricks:
                        b.fall()

                if x - X > 2 and x - X <= 4:
                    self.xv += 1
                elif X - x > 2 and X - x <= 4:
                    self.xv -= 1
                elif x - X > 4:
                    self.xv += 2
                elif X - x > 4:
                    self.xv -= 2

                if self._grab:
                    self.utils.play = False

    def brickCollision(self, brick):
        y = self.y + self.yv
        x = self.x

        if (y == brick.y):
            if (x >= brick.x and x <= brick.x + brick.w - 1):
                brick.hit(self, self._thru, self._fire)
                if not self._thru:
                    self.yv = -self.yv
                return

        y = self.y
        x = self.x + self.xv

        if (y == brick.y):
            if (x >= brick.x and x <= brick.x + brick.w - 1):
                brick.hit(self, self._thru, self._fire)
                if not self._thru:
                    self.xv = -self.xv
                return

        y = self.y + self.yv
        x = self.x + self.xv

        if (y == brick.y):
            if (x >= brick.x and x <= brick.x + brick.w - 1):
                brick.hit(self, self._thru, self._fire)
                if not self._thru:
                    self.xv = -self.xv
                    self.yv = -self.yv
                return

    def speedUp(self):
        self.xv *= 2
        self.yv *= 2

    def slowDown(self):
        self.xv //= 2
        self.yv //= 2

    def split(self):
        b1 = Ball(self.game, self.x, self.y, 2*self.xv,
                  self.yv, self._thru, self._fire)
        b2 = Ball(self.game, self.x, self.y, -1*self.xv,
                  self.yv, self._thru, self._fire)
        self.game.balls.append(b1)
        self.game.balls.append(b2)
        self.game.balls.remove(self)

    def setThru(self, val):
        self._thru = val

    def setGrab(self, val):
        self._grab = val

    def setFire(self, val):
        self._fire = val

    def dead(self):
        if self.y > Y0:
            return True
        return False
