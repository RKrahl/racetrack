#! /usr/bin/python
# 
# Test the racetrack package with the example from c't magazine:
# Harald Boegeholz, vertrac't, Knobelaufgabe: c't-Racetrackc't,
# c't 23/15, P. 48, http://heise.de/-2845878
#

from __future__ import print_function
import logging
from Tkinter import *
import racetrack
from racetrack.linalg import *
from racetrack.track import Track
from racetrack.tk import TrackView
from racetrack.car import Car
from racetrack.backtrack import SlowMotionBacktrack

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(sticky=NSEW)
        self.createTrack()
        self.createWidgets()
        self.car = Car(self.track)
        log.info('Search a simple path using SlowMotionBacktrack ...')
        backtrack = SlowMotionBacktrack(self.car)
        backtrack.search()
        log.info('Found a path with %d steps.' % len(self.car.path))
        self.trackview.drawPath(self.car.path, tags=['car'])

    def createTrack(self):
        log.info('Create track ...')

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

        barriers = [ LineSegment(p1, p2), LineSegment(p2, p3), 
                     LineSegment(p3, p4),
                     LineSegment(p5, p6),
                     LineSegment(p7, p8), LineSegment(p8, p9),
                     LineSegment(p10, p9), LineSegment(p9, p11) ]
        start = Point(120, 180)
        finish = Point(320, 220)
        self.track = Track(499, 399, start, finish, barriers)

    def createWidgets(self):
        top = self.winfo_toplevel()
        top.title('Race Track')
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.menuBar = Menu(top)
        top['menu'] = self.menuBar
        self.fileMenu = Menu(self.menuBar)
        self.menuBar.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_command(label='Quit', command=self.quit, 
                                  accelerator="Ctrl-q")
        self.viewMenu = Menu(self.menuBar)
        self.menuBar.add_cascade(label='View', menu=self.viewMenu)

        self.trackview = TrackView(self, self.track, 
                                   borderwidth=2, relief=GROOVE)
        self.trackview.grid(row=0, column=0, sticky=NSEW)

        self.xscroll = Scrollbar(self, orient=HORIZONTAL, 
                                 command=self.trackview.xview)
        self.yscroll = Scrollbar(self, orient=VERTICAL, 
                                 command=self.trackview.yview)
        self.xscroll.grid(row=1, column=0, sticky=EW)
        self.yscroll.grid(row=0, column=1, sticky=NS)

        self.trackview['xscrollcommand'] = self.xscroll.set
        self.trackview['yscrollcommand'] = self.yscroll.set

        self.viewMenu.add_command(label='Zoom in', 
                                  command=self.trackview.zoomIn, 
                                  accelerator="Ctrl-+")
        self.viewMenu.add_command(label='Zoom out', 
                                  command=self.trackview.zoomOut, 
                                  accelerator="Ctrl--")

        self.bind_all("<Control-q>", lambda e:self.quit())
        self.bind_all("<Control-plus>", self.trackview.zoomIn)
        self.bind_all("<Control-minus>", self.trackview.zoomOut)

app = Application()
app.mainloop()
