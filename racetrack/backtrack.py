"""Search solutions with backtracking.
"""


from racetrack.linalg import *
import racetrack.car
from racetrack.exception import RuleViolationError


class SlowMotionBacktrack(object):
    """A backtrack strategy that restricts itself to very slow motions.

    Due to the restriction, this will certainly not find an optimal
    solution most of the times.  But it will at least find a solution
    without too much erratically wandering about.
    """

    def __init__(self, car):
        self.car = car
        self.finish = car.track.finish
        self.stack = []
        self.step = -1

    def searchstep(self):

        # From the current position, consider all possible moves and
        # push them to the search stack.
        self.step += 1
        direct = self.finish - self.car.pos
        if direct == Vector(0,0) or not self.stickSearchDir:
            searchDir = direct
        else:
            searchDir = self.searchDir
        if searchDir.x > 0 and searchDir.y >= 0:
            dirs = [ Vector(0,-1),Vector(-1,0),Vector(0,1),Vector(1,0) ]
        elif searchDir.x <= 0 and searchDir.y > 0:
            dirs = [ Vector(1,0),Vector(0,-1),Vector(-1,0),Vector(0,1) ]
        elif searchDir.x < 0 and searchDir.y <= 0:
            dirs = [ Vector(0,1),Vector(1,0),Vector(0,-1),Vector(-1,0) ]
        elif searchDir.x >= 0 and searchDir.y < 0:
            dirs = [ Vector(-1,0),Vector(0,1),Vector(1,0),Vector(0,-1) ]
        else:
            dirs = [ Vector(0,0) ]
        self.searchDir = dirs[-1]
        for d in dirs:
            self.stack.append( (self.step, d) )

        # pop a possible move from the stack and try it.  Repeat if
        # the move fails.
        while True:
            try:
                (step, d) = self.stack.pop()
            except IndexError:
                raise RuntimeError("No solution found.")
            if step != self.step:
                self.step = step
                self.car.reset(step)
                self.searchDir = d
            if (d != Vector(0,0) and (self.car.pos + d) in self.car.path):
                continue
            try:
                self.car.move(d)
                self.stickSearchDir = (d != self.searchDir)
            except RuleViolationError:
                pass
            else:
                break

    def search(self):
        self.searchDir = Vector(0,0)
        self.stickSearchDir = False
        while not self.car.finished():
            self.searchstep()

