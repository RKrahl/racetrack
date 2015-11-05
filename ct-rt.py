#! /usr/bin/python
# 
# Test the racetrack package with the example from c't magazine:
# Harald Boegeholz, vertrac't, Knobelaufgabe: c't-Racetrackc't,
# c't 23/15, P. 48, http://heise.de/-2845878
#

from __future__ import print_function
import racetrack
from racetrack.linalg import *
from racetrack.track import Track
from racetrack.car import Car
from racetrack.backtrack import SlowMotionBacktrack

p1 = Point(200, 100)
p2 = Point(100, 100)
p3 = Point(100, 200)
p4 = Point(200, 200)
p5 = Point(250, 200)
p6 = Point(250, 300)
p7 = Point(400, 100)
p8 = Point(300, 100)
p9 = Point(300, 200)
p10 = Point(400, 200)
p11 = Point(300, 300)

barriers = [ LineSegment(p1, p2), LineSegment(p2, p3), LineSegment(p3, p4),
             LineSegment(p5, p6),
             LineSegment(p7, p8), LineSegment(p8, p9),
             LineSegment(p10, p9), LineSegment(p9, p11) ]
track = Track(499, 399, Point(120, 180), Point(320, 220), barriers)
car = Car(track)
backtrack = SlowMotionBacktrack(car)
backtrack.search()

print("Found a track in %d steps:\n" % len(car.path))
for  p in car.path:
    print("%d, %d" % p)
