"""Search solutions with backtracking.
"""


from racetrack.linalg import *
import racetrack.car
from racetrack.rules import isAccelerationAllowed
from racetrack.exception import RuleViolationError, NoSolutionError


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
                raise NoSolutionError()
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


class ConstraintBacktrack(object):
    """A backtrack strategy with constraints.

    A full backtrack algorithm that can be constraint to a starting
    path and a maximum number of steps to solution.
    """

    def __init__(self, car, maxsteps = None):
        self.car = car
        self.finish = car.track.finish
        self.stack = []
        self.step = len(car.path) - 2
        self.maxsteps = maxsteps
        # compile a list of all allowed accelerations.
        self._accel = filter(isAccelerationAllowed, 
                             [Vector(x,y) 
                              for x in range(-10,11) 
                              for y in range(-10,11)])
        self.solution = None

    def searchstep(self):

        def diststep(a):
            step = self.car.pos + self.car.velocity + a
            return (self.finish - step).norm2()

        # From the current position, consider all possible moves and
        # push them to the search stack.
        self.step += 1
        if self.maxsteps is None or self.step < self.maxsteps:
            self._accel.sort(key=diststep, reverse=True)
            for a in self._accel:
                d = self.car.velocity + a
                self.stack.append( (self.step, d) )

        # pop a possible move from the stack and try it.  Repeat if
        # the move fails.
        while True:
            try:
                (step, d) = self.stack.pop()
            except IndexError:
                raise NoSolutionError()
            if step != self.step:
                self.step = step
                self.car.reset(step)
            try:
                self.car.move(d)
            except RuleViolationError:
                pass
            else:
                break

    def searchNextSolution(self):
        while True:
            self.searchstep()
            if self.car.finished():
                break
        self.solution = list(self.car.path)
        self.maxsteps = len(self.solution) - 2

    def search(self):
        while True:
            try:
                self.searchNextSolution()
            except NoSolutionError:
                if self.solution is not None:
                    self.car.path = self.solution
                    break
                else:
                    raise
