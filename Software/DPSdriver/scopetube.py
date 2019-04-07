from Tkinter import Canvas, ALL

from constants import XDIV, YDIV, GRIDDASH, GRIDCOL, VCOL, CCOL, PCOL, MINSAMPLETIME, TPOS, VPOS, CPOS, PPOS

from dpsfile import Dpsfile


class Scopetube(Canvas):
    def __init__(self, root, data, horizontaljoin=False, ratiocallback=None, buttoncallback=None):
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
        if self.ratiocallback:
            nv = [-self.winheight/YDIV/m for m in self.ym]+self.y0+[self.winwidth/XDIV/self.tm, self.t0]
            nv = self.ena+[round(v, 2) for v in nv]
            self.ratiocallback(nv)

    def gety(self, vcp, i):
        i -= 1
        return (vcp-self.y0[i])*self.ym[i]+self.winheight

    def getxt(self,  t):
        return (t-self.t0)*self.tm

    def resetpoints(self):
        del self.points[:]
        self.redraw()

    def addpoint(self, p):
        self.points.append(p)
        if len(self.points) > 1:
            self.drawseg(self.points[-2], self.points[-1])

    def redraw(self):
        self.delete(ALL)
        self.drawgrid()
        self.drawsignals()

    def drawgrid(self):
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
        return round(self.smpt, 1)

    def drawsignals(self):
        for p0, p1 in zip(self.points[0:-1], self.points[1:]):
            self.drawseg(p0, p1)

    def drawseg(self, p0, p1):
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
        self.movex = event.x
        self.movey = event.y

    def bndbtnmove(self, event):
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
        self.sendnewsettings()

    def bndbtnzoom(self, event):
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
        if self.buttoncallback:
            t = [round(event.x/self.tm+self.t0, 2)]
            y = []
            for y0, ym, en in zip(self.y0, self.ym, self.ena):
                if en:
                    y.append(round((event.y-self.winheight)/ym+y0, 2))
                else:
                    y.append(-1)
            self.buttoncallback(t+y)

    def load(self,  fname):
        del self.points[:]
        self.dpsfile.load(fname)
        self.redraw()

    def save(self, fname):
        self.dpsfile.save(fname)


if __name__ == '__main__':
    from Tkinter import Tk
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
