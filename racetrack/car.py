"""Represent a car in the race.
"""


from racetrack.linalg import *
import racetrack.track
from racetrack.rules import isAccelerationAllowed


class AccelerationNotAllowed(Exception):

    def __init__(self, acceleration):
        self.acceleration = acceleration
        msg = ("Acceleration %s is beyond permissible bounds" % 
               (str(acceleration)))
        super(AccelerationNotAllowed, self).__init__(msg)

class Car(object):

    def __init__(self, track):
        self.track = track
        self.path = [ track.start ]
        self.pos = track.start
        self.velocity = Vector(0, 0)

    def finished(self):
        """True if stopped in the finish.
        """
        return self.pos == self.track.finish and self.velocity == Vector(0, 0)

    def move(self, n):
        """Make a move.  Raises an error if the move is not legal.
        """
        if isinstance(n, Point):
            newpos = n
        elif isinstance(n, Vector):
            newpos = self.pos + n
        else:
            raise TypeError("move expects either a Point or a Vector.")
        move = LineSegment(self.pos, newpos)
        self.track.checkCollision(move)
        newvel = move.getVector()
        acceleration = newvel - self.velocity
        if not isAccelerationAllowed(acceleration):
            raise AccelerationNotAllowed(acceleration)
        self.path.append(newpos)
        self.pos = newpos
        self.velocity = newvel

    def reset(self, step):
        """Reset the car to an earlier position from its path.
        """
        if not (0 <= step < len(self.path)):
            raise RuntimeError("Can not reset to step %d." % step)
        self.path = self.path[:step+1]
        self.pos = self.path[step]
        if step > 0:
            self.velocity = self.path[step] - self.path[step-1]
        else:
            self.velocity = Vector(0, 0)
