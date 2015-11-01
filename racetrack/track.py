"""Provide the track.

This module defines the track, that is the playground for the game.  
"""


from numbers import Integral
from racetrack.linalg import *


class Collision(Exception):

    def __init__(self, move, barrier, point):
        self.move = move
        self.barrier = barrier
        self.point = point
        msg = ("Collision of move %s with barrier %s at point %s"
               % (move, barrier, point))
        super(Collision, self).__init__(msg)


class Track(object):

    def __init__(self, width, height, start, finish, barriers=[]):
        if not (isinstance(width, Integral) and isinstance(height, Integral)):
            raise TypeError("Track bounds must be integral numbers.")
        if not (width > 0 and height > 0):
            raise ValueError("Track bounds must be larger then zero.")
        if not (isinstance(start, Point) and start.isIntegral() and
                isinstance(finish, Point) and finish.isIntegral()):
            raise TypeError("start and finish must be Points "
                            "with integral coordinates.")
        if not (0 < start.x <= width and 0 < start.y <= height and 
                0 < finish.x <= width and 0 < finish.y <= height):
            raise ValueError("start and finish must be within Track bounds.")

        self.start = start
        self.finish = finish

        p0 = Point(x=0, y=0)
        p1 = Point(x=width+1, y=0)
        p2 = Point(x=width+1, y=height+1)
        p3 = Point(x=0, y=height+1)
        # Add the borders of the track area as barriers.
        self.barriers = [ LineSegment(p0, p1), LineSegment(p1, p2), 
                          LineSegment(p2, p3), LineSegment(p3, p0) ]
        self.addBarriers(barriers)

    def addBarriers(self, barriers):
        self.barriers.extend(barriers)

    def checkCollision(self, move):
        for barrier in self.barriers:
            p = move & barrier
            if p:
                raise Collision(move, barrier, p)
