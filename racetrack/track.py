"""Provide the track.

This module defines the track, that is the playground for the game.  
"""


from numbers import Integral
from racetrack.linalg import *
from racetrack.exception import CollisionError


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

    def bbox(self):
        """Return the size of the track.

        The return value is a tuple (x0, y0, x1, y1) describing a
        rectangle that encloses all barriers (including the boundary)
        of the track.
        """
        xmin = None
        xmax = None
        ymin = None
        ymax = None
        for l in self.barriers:
            for p in (l.p0, l.p1):
                if xmin is None or p.x < xmin:
                    xmin = p.x
                if xmax is None or p.x > xmax:
                    xmax = p.x
                if ymin is None or p.y < ymin:
                    ymin = p.y
                if ymax is None or p.y > ymax:
                    ymax = p.y
        return (xmin, ymin, xmax, ymax)

    def checkCollision(self, move):
        for barrier in self.barriers:
            p = move & barrier
            if p:
                raise CollisionError(move, barrier, p)
