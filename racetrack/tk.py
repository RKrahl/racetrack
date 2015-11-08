"""Graphical user interface elements for Racetrack using the Tk interface.
"""

import Tkinter as tk


class TrackView(tk.Canvas):
    """A visualization widget for the race track.
    """

    gridspace = 10

    def __init__(self, parent, track, **kwargs):
        # Setup the coefficients for the internal methods _canvx() and
        # _canvy() that translate of track coordinates to canvas
        # coordinates.  The formula are:
        #   canvx = cx0 + cxsc * trackx
        #   canvy = cy0 + cysc * tracky
        # Note that in canvas coordinates, the y axis points
        # downwards, while in track coordinates it points upwards.
        # The canvas origin is at (xmin, ymax).
        (xmin, ymin, xmax, ymax) = track.bbox()
        self._cxsc = self.gridspace
        self._cysc = - self.gridspace
        self._cx0 = - (self._cxsc * xmin)
        self._cy0 = - (self._cysc * ymax)

        # Setup the canvas widget.
        cw = self._canvx(xmax)
        ch = self._canvy(ymin)
        tk.Canvas.__init__(self, parent, background='white', 
                           width=cw, height=ch, 
                           scrollregion=(-1, -1, cw+2, ch+2), 
                           **kwargs)

        # Draw the background grid.
        for x in range(xmin, xmax+1):
            cx = self._canvx(x)
            cy0 = self._canvy(ymin)
            cy1 = self._canvy(ymax)
            self.create_line(cx, cy0, cx, cy1, fill='#ddd', tags='grid')
        for y in range(ymin, ymax+1):
            cx0 = self._canvx(xmin)
            cx1 = self._canvx(xmax)
            cy = self._canvy(y)
            self.create_line(cx0, cy, cx1, cy, fill='#ddd', tags='grid')

        # Draw the barriers.  This also includes the outer boundary.
        for l in track.barriers:
            self.create_line(self._canvx(l.p0.x), self._canvy(l.p0.y), 
                             self._canvx(l.p1.x), self._canvy(l.p1.y), 
                             fill='black', width=3, capstyle=tk.ROUND, 
                             tags='barrier')

        # Draw start and finish.
        cx = self._canvx(track.start.x)
        cy = self._canvy(track.start.y)
        self.create_oval(cx-6, cy-6, cx+6, cy+6, 
                         fill='#c00', outline='', tags='start')
        cx = self._canvx(track.finish.x)
        cy = self._canvy(track.finish.y)
        self.create_oval(cx-6, cy-6, cx+6, cy+6, 
                         fill='#0c0', outline='', tags='finish')

    def _canvx(self, trackx):
        """Return the canvas x coordinate corresponding to trackx.
        """
        return self._cx0 + self._cxsc * trackx

    def _canvy(self, tracky):
        """Return the canvas y coordinate corresponding to tracky.
        """
        return self._cy0 + self._cysc * tracky

    def drawPath(self, path, fill='blue', width=3, capstyle=tk.ROUND, tags=[]):
        coords = []
        for p in path:
            coords.extend((self._canvx(p.x),self._canvy(p.y)))
        tags.append('path')
        self.create_line(coords, fill=fill, width=width, capstyle=capstyle, 
                         tags=tags)

