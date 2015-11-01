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
        if direct == Vector(0,0):
            # finish reached, stand still.
            self.stack.append( (self.step, Vector(0,0)) )
        else:
            if direct.x > 0:
                if direct.y >= 0:
                    dirs = [Vector(-1,0),Vector(0,-1),Vector(0,1),Vector(1,0)]
                else:
                    dirs = [Vector(-1,0),Vector(0,1),Vector(0,-1),Vector(1,0)]
            elif direct.x < 0:
                if direct.y >= 0:
                    dirs = [Vector(1,0),Vector(0,-1),Vector(0,1),Vector(-1,0)]
                else:
                    dirs = [Vector(1,0),Vector(0,1),Vector(0,-1),Vector(-1,0)]
            else:
                if direct.y > 0:
                    dirs = [Vector(0,-1),Vector(-1,0),Vector(1,0),Vector(0,1)]
                else:
                    dirs = [Vector(0,1),Vector(-1,0),Vector(1,0),Vector(0,-1)]
            for d in dirs:
                if (self.car.pos + d) not in self.car.path:
                    self.stack.append( (self.step, d) )
        # pop a possible move from the stack and try it.  Repeat if
        # the move fails.
        while True:
            try:
                (step, dir) = self.stack.pop()
            except IndexError:
                raise RuntimeError("No solution found.")
            if step != self.step:
                self.step = step
                self.car.reset(step)
            try:
                self.car.move(dir)
            except RuleViolationError:
                pass
            else:
                break

    def search(self):
        while not self.car.finished():
            self.searchstep()

