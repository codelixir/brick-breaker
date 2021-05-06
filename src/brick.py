import colorama
from colorama import Fore, Back, Style

# custom modules
from constants import brickCOLOR, Y0
from power import getPowerUp


def winCondition(bricks):
    if not bricks:
        return True
    for b in bricks:
        if not b.unbreakable():
            return False
    return True


class Brick:
    def __init__(self, game, x, y, strength):
        self.utils = game.utils
        self.game = game
        self.x = x
        self.y = y
        self._strength = strength
        self._color = brickCOLOR[strength]
        self.w = 5
        self._char = ' '

    def display(self):
        y = self.y
        w = self.w
        arr = self.game.board
        for x in range(self.x, self.x+w):
            arr[y][x] = self._color + self._char
        arr[y][self.x + w] = Style.RESET_ALL + arr[y][self.x + w]
        self.game.board = arr

    def hit(self, ball, thru=False, fire=False):
        if thru:
            self._strength = 0
        else:
            if self._strength:
                self._strength -= 1

        if self._strength >= 0:
            self._color = brickCOLOR[self._strength]
            getPowerUp(self, ball)

    def explode(self, ball):
        # hit neighbors
        for b in self.game.bricks[:]:
            if b != self:
                # sideways neighbors
                if b.y == self.y:
                    if (b.x + b.w == self.x) or (self.x + self.w == b.x):
                        b.hit(ball)
                # other neighbours
                elif (b.y == self.y - 1) or (b.y == self.y + 1):
                    if (b.x >= self.x - b.w - 1) and (b.x <= self.x + self.w + 1):
                        b.hit(ball)
        self._strength = 0

    def destroyed(self):
        if self._strength == 0:
            return True
        return False

    def unbreakable(self):
        return (self._strength < 0)

    def fall(self):
        self.y += 1
        if (self.y == Y0):
            self.utils.lives = 0


class Explosive(Brick):
    def __init__(self, game, x, y, strength=4):
        super().__init__(game, x, y, strength)

    def hit(self, ball, thru=False, fire=False):
        self.explode(ball)


class Rainbow(Brick):
    def __init__(self, game, x, y, strength=3):
        super().__init__(game, x, y, strength)

    def display(self):
        self._strength = self._strength % 3 + 1
        self._color = brickCOLOR[self._strength]
        y = self.y
        w = self.w
        arr = self.game.board
        for x in range(self.x, self.x+w):
            arr[y][x] = self._color + self._char
        arr[y][self.x + w] = Style.RESET_ALL + arr[y][self.x + w]
        self.game.board = arr

    def hit(self, ball, thru=False, fire=False):
        if fire:
            self.explode(ball)
        elif not thru:
            self.game.bricks.append(
                Brick(self.game, self.x, self.y, self._strength))
        self._strength = 0
        self._color = brickCOLOR[self._strength]
