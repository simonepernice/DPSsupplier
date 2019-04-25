# coding: utf-8

"""
DPS scope

This is the DPS scope interface with settings regulations.
It is used to display polling wave on DPS output or 
to edit a waveform.

(C)2019 - Simone Pernice - pernice@libero.it

This file is part of DPSinterface.

DPSinterface is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 3.

DPSinterface is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DPSinterface.  If not, see <http://www.gnu.org/licenses/>.
This is distributed under GNU LGPL license, see license.txt

"""

from constants import XDIV, YDIV, GRIDDASH, GRIDCOL, VCOL, CCOL, PCOL, MINSAMPLETIME, TPOS, VPOS, CPOS, PPOS
from dpsfile import Dpsfile

try:
    from Tkinter import Canvas, ALL
except ImportError:
    from tkinter import Canvas, ALL

__author__ = "Simone Pernice"
__copyright__ = "Copyright 2019, DPS supplier"
__credits__ = ["Simone Pernice"]
__license__ = "GNU GPL v3.0"
__version__ = "0.9.0"
__date__ = "16 April 2019"
__maintainer__ = "Simone Pernice"
__email__ = "perniceb@libero.it"
__status__ = "Development"

class Scopetube(Canvas):
    """
    Scopetube is class used to represent the monitor of a scope where the curves are plot.

    """
    def __init__(self, root, data, horizontaljoin=False, ratiocallback=None, buttoncallback=None):
        """
        Create a new scopetube.

        :param root: is the main window
        :param data: is the data to display (or update if enabled)
        :param horizontaljoin: if true the points are joined through horizontal segments then vertica 
        (for waveditor) if it is false they are just joined as useful in the scope view
        :param buttoncallback: it is the function to provide if the user can manage the graphs 
        changing point (for wave editor)
        :returns: a new instance of scope

        """ 
        Canvas.__init__(self, root, background='white')

        self.bind('<Button-1>', self.bndbtnmovebegin)
        self.bind('<B1-Motion>', self.bndbtnmove)
        self.bind('<ButtonRelease-1>', self.bndbtnmoveend)

        self.bind('<Button-2>', self.bndbtnfit)

        self.bind('<Button-4>', self.bndbtnzoom)
        self.bind('<Button-5>', self.bndbtnzoom)
        root.bind('<MouseWheel>', self.bndbtnzoom)  # do not understand why if bind to this canvas does not catch the mousewheel

        self.bind('<ButtonRelease-3>', self.bndbtnpntins)

        self.horizontaljoin = horizontaljoin

        self.points = data
        self.dpsfile = Dpsfile(self.points)

        self.ratiocallback = ratiocallback

        self.buttoncallback = buttoncallback

    def setratios(self, data):
        """
        It is called by the user to set the view ratios

        :param data: are the new settings:  v, c, p enables; v, c, p initial value; v, c, p divisions; t initial value and divisions.

        """ 
        self.ena = data[0:3]

        self.winheight = float(self.winfo_height())
        self.ym = [-self.winheight/YDIV/a for a in data[3:6]]
        self.y0 = data[6:9]

        self.winwidth = float(self.winfo_width())
        self.tm = self.winwidth/XDIV/data[9]
        self.t0 = data[10]

        self.smpt = 1./self.tm
        if self.smpt < MINSAMPLETIME:
            self.smpt = MINSAMPLETIME

    def sendnewsettings(self):
        """
        It is called to send the new settings back to the father.
        """ 
        if self.ratiocallback and self.winfo_ismapped() : # Check if it is mapped is very important otherwise it may hang if catch a scale modification but the windows is not made
            nv = [-self.winheight/YDIV/m for m in self.ym]+self.y0+[self.winwidth/XDIV/self.tm, self.t0]
            nv = self.ena+[round(v, 2) for v in nv]
            self.ratiocallback(nv)

    def gety(self, vcp, i):
        """
        Compute the y [pixels] from its voltage/current/power based on the index

        :param vcp: voltage, curren or pawer to convert in pixel
        :param i: type to convert: 1 is voltage, 2 current, 3 power
        :returns: the pixels position

        """
        i -= 1
        return (vcp-self.y0[i])*self.ym[i]+self.winheight

    def getxt(self,  t):
        """
        Compute the x [pixels] from its time

        :param t: the time in seconds
        :returns: the pixels position in x

        """
        return (t-self.t0)*self.tm

    def resetpoints(self):
        """
        Delete all the points of the waveform and clean the screen

        """
        del self.points[:]
        self.redraw()

    def addpoint(self, p):
        """
        Add a new point at the end of the current list

        :param p: the pint to add: [time, voltage, current, power]
        """
        self.points.append(p)
        if len(self.points) > 1:
            self.drawseg(self.points[-2], self.points[-1])

    def redraw(self):
        """
        Redraw everythin on the screen
        """
        self.delete(ALL)
        self.drawgrid()
        self.drawsignals()

    def drawgrid(self):
        """
        Redraw the grid on the screen
        """
        xmax = self.winwidth
        ymax = self.winheight
        dx = xmax/XDIV
        dy = ymax/YDIV

        x = 0.
        for i in range(int(XDIV)+1):
            self.create_line(x, 0, x, ymax, fill=GRIDCOL, dash=GRIDDASH)
            x += dx

        y = 0.
        for i in range(int(YDIV)+1):
            self.create_line(0, y, xmax, y, fill=GRIDCOL, dash=GRIDDASH)
            y += dy

    def sampletime(self):
        """
        Returns the sample time to have a sample per pixel
        """
        return round(self.smpt, 1)

    def drawsignals(self):
        """
        Redraw the signals on the screen
        """
        for p0, p1 in zip(self.points[0:-1], self.points[1:]):
            self.drawseg(p0, p1)

    def drawseg(self, p0, p1):
        """
        Draw a segment between point p0 and p1
        
        :param p0: the pint where the segment begins (time, voltage, current, power)
        :param p1: the pint where the segment ends (time, voltage, current, power)
        """
        x0 = self.getxt(p0[TPOS])
        x1 = self.getxt(p1[TPOS])

        for i, c, en in zip((VPOS, CPOS, PPOS), (VCOL, CCOL, PCOL), self.ena):
            if en and len(p0) > i:
                y0 = self.gety(p0[i], i)
                y1 = self.gety(p1[i], i)

                if self.horizontaljoin:
                    self.create_line(x0, y0, x1, y0, fill=c)
                    self.create_line(x1, y0, x1, y1, fill=c)
                else:
                    self.create_line(x0, y0, x1, y1, fill=c)

    def bndbtnmovebegin(self, event):
        """
        Store the point where a drag begins (left button)
        
        :param event: the point where drag begins
        """
        self.movex = event.x
        self.movey = event.y

    def bndbtnmove(self, event):
        """
        While the button is pressed the view of the graphs is updated
        
        :param event: the point where drag continues
        """
        enabled = 0
        delta = event.y-self.movey

        for i, ym, en in zip(range(3), self.ym, self.ena):
            if en:
                enabled += 1
                self.y0[i] -= delta/ym
        self.movey = event.y

        if enabled > 0:
            delta = event.x-self.movex
            self.t0 -= delta/self.tm
            self.movex = event.x

            self.redraw()

    def bndbtnmoveend(self, event):
        """
        When the drag is done the main user interface is updated with new scales and initial points.
        
        :param event: the point where drag begins
        """
        self.sendnewsettings()

    def bndbtnzoom(self, event):
        """
        When the wheel is ritated the zoom on time, with shift on amplitude, with ctrl enable change is performed
        
        :param event: the wheel rotation seen as button on *nix or delta on Windows
        """        
        if event.num == 4 or event.delta > 0:
            k = 2
            k2 = 1
        elif event.num == 5 or event.delta < 0:
            k = 0.5
            k2 = -1
        else:
            return

        # shift pressed bndbtnzoom on Y
        if event.state & 0x0001:
            for i, en in zip(range(3), self.ena):
                if en:
                    self.ym[i] *= k

        # control pressed switch enabled waveform
        elif event.state & 0x0004:
            # convert enables to bits
            a = 0
            s = 1
            for e in self.ena:
                if e:
                    a |= s
                s <<= 1

            a += k2

            # convert bits to enables
            s = 1
            for i in range(3):
                self.ena[i] = 1 if a & s else 0
                s <<= 1

        # nothing pressed bndbtnzoom on X
        else:
            self.tm *= k

        self.sendnewsettings()
        self.redraw()

    def bndbtnfit(self, event):
        """
        When the drag is done the main user interface is updated with new scales and initial points.
        
        :param event: the point where drag begins
        """        
        somethingenabled = False
        for e, i in zip(self.ena,  [VPOS, CPOS, PPOS]):
            if e and len(self.points) > 0:
                somethingenabled = True
                if i >= len(self.points[0]):
                    continue
                mi = mx = self.points[0][i]
                for p in self.points[1:]:
                    pi = p[i]
                    if pi < mi:
                        mi = pi
                    elif pi > mx:
                        mx = pi
                self.y0[i-1] = mi
                if mx > mi:
                        self.ym[i-1] = -self.winheight/(mx-mi)

        if somethingenabled and len(self.points) > 0:
            mi = mx = self.points[0][TPOS]
            for p in self.points[1:]:
                pi = p[TPOS]
                if pi < mi:
                    mi = pi
                elif pi > mx:
                    mx = pi
            self.t0 = mi
            if (mx > mi):
                    self.tm = self.winwidth/(mx-mi)

            self.sendnewsettings()
            self.redraw()

    def bndbtnpntins(self, event):
        """
        When the right button is pressed a new point is inserted. With shift the next point is modified in amplitude as the cursor, 
        with ctrl the next is deleted, with shift + ctrl the next point is replaced by the current position
        
        :param event: the point where drag begins
        """
        if self.buttoncallback:
            t = [round(event.x/self.tm+self.t0, 2)]
            y = []
            for y0, ym, en in zip(self.y0, self.ym, self.ena):
                if en:
                    y.append(round((event.y-self.winheight)/ym+y0, 2))
                else:
                    y.append(-1)
            # Shift and CTRL pressed modify the next point with current
            if event.state & 1 and event.state & 4:
                self.buttoncallback(t+y, action='delete')
                self.buttoncallback(t+y, action='insert')
            # Shift pressed modify the next point amplitude with current
            elif event.state & 1:
                self.buttoncallback(t+y, action='modify')
            # Ctrl pressed delete the next point
            elif event.state & 4:
                self.buttoncallback(t+y, action='delete')
            # Insert a new point
            else:
                self.buttoncallback(t+y, action='insert')

    def load(self,  fname):
        """
        Load waveform data saved before from a file (CSV format: time, voltage, current, power).

        :param fname: the file name to load
        """
        del self.points[:]
        self.dpsfile.load(fname)
        self.redraw()

    def save(self, fname):
        """
        Save current waveform into a file (CSV format: time, voltage, current, power).

        :param fname: the file name to save
        """
        self.dpsfile.save(fname)


if __name__ == '__main__':
    try:
        from Tkinter import Tk
    except ImportError:
        from tkinter import Tk

    root = Tk()
    from random import random

    data = []
    for index in range(100):
        v = abs(10*random())
        i = abs(10*random())
        data.append([index*10, v, i, v*i])

    my_gui = Scopetube(root, data, False)

    my_gui.pack()

    my_gui.update()

    my_gui.setratios(
        [1, 1, 1,
         1, 1, 1,
         0, 0,  0,
         60, 0]
    )

    my_gui.redraw()

    root.mainloop()
