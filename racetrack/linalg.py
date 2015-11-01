"""Define the linear algebra needed for the game.

This module defines some linear algebra objects that are the building
blocks of the game.  Essentially, this is an affine two dimensional
space.  E.g. points, vectors, and line segments, where a vector is the
difference of two points and a line segment is defined by a starting
and an end point.

>>> v = Vector(x=3, y=4)
>>> v
Vector(x=3, y=4)
>>> v == Vector(x=3, y=4)
True
>>> v == Vector(x=3, y=5)
False
>>> v != Vector(x=3, y=4)
False
>>> v != Vector(x=3, y=5)
True
>>> v.norm1()
7.0
>>> v.norm2()
5.0
>>> v.norminf()
4.0
>>> -v
Vector(x=-3, y=-4)
>>> w = Vector(x=1, y=-2)
>>> w
Vector(x=1, y=-2)
>>> v + w
Vector(x=4, y=2)
>>> v - w
Vector(x=2, y=6)
>>> 0.25 * v
Vector(x=0.75, y=1.0)
>>> p = Point(x=15, y=12)
>>> p
Point(x=15, y=12)
>>> p + v
Point(x=18, y=16)
>>> p - v
Point(x=12, y=8)
>>> (p + v) - v == p
True
>>> q = Point(x=7, y=-9)
>>> q
Point(x=7, y=-9)
>>> p - q
Vector(x=8, y=21)
>>> p + (q - p) == q
True
>>> (p + v) - p == v
True
>>> p + q
Traceback (most recent call last):
  ...
TypeError: unsupported operand type(s) for +: 'Point' and 'Point'
>>> l1 = LineSegment(Point(x=-1, y=-2), Point(x=5, y=1))
>>> l1
LineSegment(Point(x=-1, y=-2), Point(x=5, y=1))
>>> l2 = LineSegment(Point(x=0, y=0) - Vector(x=1, y=2), Vector(x=6, y=3))
>>> l2 == l1
True
>>> l3 = LineSegment(Point(x=2, y=-2), Vector(x=-3, y=3))
>>> l1 & l3
Point(x=1.0, y=-1.0)
>>> l4 = LineSegment(Point(x=1, y=1), Vector(x=2, y=1))
>>> l1 & l4 is None
True
>>> l1 & LineSegment(Point(x=7, y=2), Vector(x=2, y=1)) is None
True
>>> l1 & LineSegment(Point(x=7, y=2), -Vector(x=2, y=1)) == Point(x=5, y=1)
True
>>> l1 & LineSegment(Point(x=7, y=2), Point(x=-3, y=-3)) == Point(x=-1, y=-2)
True
>>> l1 & LineSegment(Point(x=3, y=0), Vector(x=0, y=0)) == Point(x=3, y=0)
True
>>> LineSegment(Point(x=3, y=0), Vector(x=0, y=0)) & l1 == Point(x=3, y=0)
True
>>> l1 & LineSegment(Point(x=3, y=2), Vector(x=0, y=0)) is None
True
>>> LineSegment(Point(x=3, y=2), Vector(x=0, y=0)) & l1 is None
True
>>> LineSegment(p, p) == LineSegment(p, Vector(0,0))
True
>>> LineSegment(p, p) & LineSegment(p, Vector(0,0)) == p
True
>>> LineSegment(p, p) & LineSegment(q, q) is None
True

Note: in the game, the positions of the race cars must be constraint
to Points having integer coordinates.  But this is not enforced here.
"""

from __future__ import division
from numbers import Real
from collections import namedtuple
from math import fabs, sqrt


def sqr(x):
    """Return the square of x.
    """
    return x*x


class Vector(namedtuple('Vector', ['x', 'y'])):
    """A Vector is the difference between two Ponts.
    """

    def __eq__(self, other):
        """self == other."""
        if isinstance(other, Vector):
            for (s, o) in zip(self, other):
                if s != o:
                    return False
            else:
                return True
        else:
            return NotImplemented

    def __ne__(self, other):
        """self != other."""
        if isinstance(other, Vector):
            for (s, o) in zip(self, other):
                if s != o:
                    return True
            else:
                return False
        else:
            return NotImplemented

    def norm1(self):
        """one or taxicap norm."""
        return sum(map(fabs, self))

    def norm2(self):
        """two or Euclidean norm."""
        return sqrt(sum(map(sqr, self)))

    def norminf(self):
        """infinity or maximum norm."""
        return max(map(fabs, self))

    def __neg__(self):
        """-self."""
        return Vector._make([-c for c in self])

    def __add__(self, other):
        """sum of two Vectors."""
        if isinstance(other, Vector):
            return Vector._make(map(sum, zip(self, other)))
        else:
            return NotImplemented

    def __sub__(self, other):
        """difference between two Vectors."""
        if isinstance(other, Vector):
            return self + -other
        else:
            return NotImplemented

    def __rmul__(self, other):
        """scalar*Vector."""
        if isinstance(other, Real):
            return Vector._make([other*c for c in self])
        else:
            return NotImplemented


class Point(namedtuple('Point', ['x', 'y'])):
    """A Point in the space.
    """

    def __eq__(self, other):
        """self == other."""
        if isinstance(other, Point):
            for (s, o) in zip(self, other):
                if s != o:
                    return False
            else:
                return True
        else:
            return NotImplemented

    def __ne__(self, other):
        """self != other."""
        if isinstance(other, Point):
            for (s, o) in zip(self, other):
                if s != o:
                    return True
            else:
                return False
        else:
            return NotImplemented

    def __add__(self, other):
        """sum of Point and Vector."""
        if isinstance(other, Vector):
            return Point._make(map(sum, zip(self, other)))
        else:
            return NotImplemented

    def __sub__(self, other):
        """difference between a Point and either a Vector or a Point.
        The difference between a Point and a Vector is a Point.
        The difference between two Points is a Vector."""
        if isinstance(other, Vector):
            return self + -other
        elif isinstance(other, Point):
            return Vector._make([(s - o) for (s, o) in zip(self, other)])
        else:
            return NotImplemented


class LineSegment(object):
    """A line segment between a start and an end Point.
    """

    def __init__(self, p0, a):
        if isinstance(p0, Point):
            self.p0 = p0
        else:
            raise TypeError("start point must be a Point.")
        if isinstance(a, Point):
            self.p1 = a
        elif isinstance(a, Vector):
            self.p1 = p0 + a
        else:
            raise TypeError("a must be a Point or a Vector.")

    def __repr__(self):
        return "LineSegment(%s, %s)" % (self.p0, self.p1)

    def __eq__(self, other):
        """self == other."""
        if isinstance(other, LineSegment):
            return self.p0 == other.p0 and self.p1 == other.p1
        else:
            return NotImplemented

    def __ne__(self, other):
        """self != other."""
        if isinstance(other, LineSegment):
            return self.p0 != other.p0 or self.p1 != other.p1
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.p0) ^ hash(self.p1)

    def __and__(self, other):
        """intersection Point of two LineSegments, if any.
        Return None if the line segments do not intersect.
        """
        u = self.p1 - self.p0
        v = other.p1 - other.p0
        w = other.p1 - self.p0
        d = u.x * v.y - v.x * u.y
        r = w.x * v.y - v.x * w.y
        q = u.x * w.y - w.x * u.y
        if d != 0:
            # General case, the two lines intersect in one point ...
            t = r / d
            s = q / d
            if 0.0 <= t <= 1.0 and 0.0 <= s <= 1.0:
                # ... this point is within the segments, return the point.
                return self.p0 + t * u
            else:
                # ... but this point is not within both segments.
                return None
        else:
            # Degenerate cases.
            if r != 0 or q != 0:
                # Parallel lines.
                return None
            elif u.norm1() != 0:
                # self line segment is not degenerated to a single point.
                w0 = other.p0 - self.p0
                w1 = other.p1 - self.p0
                t = w0.x / u.x if u.x != 0 else w0.y / u.y
                s = w1.x / u.x if u.x != 0 else w1.y / u.y
                if (t < 0.0 and s < 0.0) or (t > 1.0 and s > 1.0):
                    # disjunct segments.
                    return None
                elif (t < 0.0 <= s) or (s < 0.0 <= t):
                    # self.p0 lies on other.
                    return self.p0
                elif t <= s:
                    # other.p0 lies on self.
                    return other.p0
                else:
                    # other.p1 lies on self.
                    return other.p1
            elif v.norm1() != 0:
                # self is degenerated to a single point, but other is not.
                w0 = self.p0 - other.p0
                t = w0.x / v.x if v.x != 0 else w0.y / v.y
                if 0.0 <= t <= 1.0:
                    # self.p0 lies on other.
                    return self.p0
                else:
                    # disjunct segments.
                    return None
            elif w.norm1() != 0:
                # Two separated single points.
                return None
            else:
                # All four points coincide.
                return self.p0
