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
from racetrack.backtrack import SlowMotionBacktrack, ConstraintBacktrack
from racetrack.exception import NoSolutionError

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
        self.solution = list(self.car.path)
        log.info('Found a solution with %d steps.' % (len(self.solution) - 1))
        self.redrawTrack()
        maxsteos = len(self.solution) - 1
        self.prefixlen.set(str(maxsteos))
        self.backtrack = ConstraintBacktrack(self.car, maxsteps=maxsteos)

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

        buttonframe = Frame(self)
        buttonframe.grid(row=2, column=0, columnspan=2)
        self.prefixlen = StringVar()
        isIntCommand = self.register(self.isInt)
        self.prefixentry = Entry(buttonframe, textvariable=self.prefixlen,
                                 width=6, validate='all',
                                 validatecommand=(isIntCommand, '%P'))
        self.prefixentry.grid(row=0, column=0, padx=10, pady=2)
        self.nextbutton = Button(buttonframe, text='Next', width=9,
                                 command=self.searchNext)
        self.nextbutton.grid(row=0, column=1, padx=10, pady=2)

        self.bind_all("<Control-q>", lambda e:self.quit())
        self.bind_all("<Control-plus>", self.trackview.zoomIn)
        self.bind_all("<Control-minus>", self.trackview.zoomOut)
        self.prefixentry.bind('<Return>', self.setPrefix)

    def isInt(self, value):
        if value == "":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False

    def redrawTrack(self):
        self.trackview.delete('car')
        self.trackview.drawPath(self.car.path, tags=['car'])

    def setPrefix(self, event):
        prefix = int(self.prefixlen.get())
        log.info('set prescribed initial path len = %d.' % prefix)
        self.car.reset(prefix)
        self.redrawTrack()
        maxsteps = len(self.solution) - 1
        self.backtrack = ConstraintBacktrack(self.car, maxsteps=maxsteps)

    def searchNext(self):
        log.info('Search a path using ConstraintBacktrack ...')
        log.info('max step = %d.' % self.backtrack.maxsteps)
        try:
            self.backtrack.searchNextSolution()
            self.solution = self.car.path[:]
            log.info('Found a solution with %d steps.' % (len(self.solution)-1))
            self.redrawTrack()
        except NoSolutionError:
            log.info('No solution found.')
            self.car.path = self.solution[:]

app = Application()
app.mainloop()
