from Tkinter import Canvas, ALL

from constants import XDIV, YDIV, GRIDDASH, GRIDCOL, VCOL, CCOL, PCOL, MINSAMPLETIME, TPOS, VPOS, CPOS, PPOS

from dpsfile import Dpsfile

class Scopetube(Canvas):
    def __init__(self, root):
        Canvas.__init__(self, root, background='white')
        
        self.v0=-1
        self.c0=-1
        self.p0=-1
        
        self.points=[]
        self.dpsfile=Dpsfile(self.points)
                
    def setratios(self, vdiv, v0, vena, cdiv, c0, cena, pdiv, p0, pena, tdiv, t0):
        self.yq=self.winfo_height()
        self.ena=(vena, cena, pena)

        self.vm=-self.yq/YDIV/vdiv        
        self.v0=v0

        self.cm=-self.yq/YDIV/cdiv
        self.c0=c0

        self.pm=-self.yq/YDIV/pdiv
        self.p0=p0

        self.tm=self.winfo_width()/XDIV/tdiv
        self.t0=t0
        self.tdiv=tdiv

        self.smpt=1./self.tm
        if self.smpt<MINSAMPLETIME:
            self.smpt=MINSAMPLETIME            

    def getyv(self,  v):
        return (v-self.v0)*self.vm+self.yq

    def getyc(self,  c):
        return (c-self.c0)*self.cm+self.yq

    def getyp(self,  p):
        return (p-self.p0)*self.pm+self.yq

    def getxt(self,  t):
        return (t-self.t0)*self.tm

    def resetpoints(self):
        del self.points[:]
        self.redraw()
    
    #a point is made by: (voltage, current, power, time)
    def addpoint(self, p):
        self.points.append(p)
        if len(self.points)>1:
            self.drawseg(self.points[-2], self.points[-1])
        
    def redraw(self):
        self.delete(ALL)
        self.drawgrid()
        self.drawsignals()

    def drawgrid(self):
        YMAX=float(self.winfo_height())
        XMAX=float(self.winfo_width())
        DX=XMAX/XDIV
        DY=YMAX/YDIV
        x=0.
        for i in range(int(XDIV)+1):
            self.create_line(x, 0, x, YMAX, fill=GRIDCOL, dash=GRIDDASH)
            x+=DX

        y=0.
        for i in range(int(YDIV)+1):
            self.create_line(0, y, XMAX, y, fill=GRIDCOL, dash=GRIDDASH)
            y+=DY

    def sampletime(self):
        return self.smpt
        
    def drawsignals(self):
        for p0, p1 in zip(self.points[0:-1], self.points[1:]):
            self.drawseg(p0, p1)
    
    def drawseg(self, p0, p1):
        x0=self.getxt(p0[TPOS])
        x1=self.getxt(p1[TPOS])
        for i, c, gety, en in zip((VPOS, CPOS, PPOS), (VCOL, CCOL, PCOL), (self.getyv, self.getyc, self.getyp), self.ena):
            if en: self.create_line(x0, gety(p0[i]), x1, gety(p1[i]), fill=c)

    def load(self,  fname):
        self.resetpoints()
        self.dpsfile.load(fname, self.addpoint)

    def save(self, fname):
        self.dpsfile.save(fname)

if __name__=='__main__':
    from Tkinter import Tk
    root=Tk()
    my_gui=Scopetube(root).pack()
    root.mainloop()
