from Tkinter import Canvas, ALL

class Scopetube(Canvas):
    XDIV=10.
    YDIV=10.
    GRIDDASH=(1, 6)
    GRIDCOL='black'
    VCOL='red'
    CCOL='green'
    PCOL='blue'
    MINSAMPLETIME=1.
    
    def __init__(self, root):
        Canvas.__init__(self, root, background='white')
        
        self.points=[]
                
    def setratios(self, vdiv, v0, vena, cdiv, c0, cena, pdiv, p0, pena, tdiv, t0):
        self.yq=self.winfo_height()
        self.ena=(vena, cena, pena)
        
        self.vm=-self.yq/Scopetube.YDIV/vdiv        
        self.vdiv=vdiv
        self.v0=v0

        self.cm=-self.yq/Scopetube.YDIV/cdiv
        self.c0=c0

        self.pm=-self.yq/Scopetube.YDIV/pdiv
        self.p0=p0

        self.tm=self.winfo_width()/Scopetube.XDIV/tdiv
        self.t0=t0
        self.tdiv=tdiv

        self.smpt=1./self.tm
        if self.smpt<Scopetube.MINSAMPLETIME:
            self.smpt=Scopetube.MINSAMPLETIME        

    def getyv(self,  v):
        return (v-self.v0)*self.vm+self.yq

    def getyc(self,  c):
        return (c-self.c0)*self.cm+self.yq

    def getyp(self,  p):
        return (p-self.p0)*self.pm+self.yq

    def getxt(self,  t):
        return (t-self.t0)*self.tm

    def resetpoints(self):
        self.points=[]
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
        YMIN=self.getyv(0)
        YMAX=self.getyv((Scopetube.YDIV+1)*self.vdiv)
        for ix in range(0, int(Scopetube.XDIV+1)):
            X=self.getxt(ix*self.tdiv+self.t0)
            self.create_line(X, YMIN, X, YMAX, fill=Scopetube.GRIDCOL, dash=Scopetube.GRIDDASH)

        XMIN=self.getxt(self.t0)
        XMAX=self.getxt((Scopetube.XDIV+1)*self.tdiv+self.t0)
        for iy in range(0, int(Scopetube.YDIV+1)):
            Y=self.getyv(iy*self.vdiv)
            self.create_line(XMIN, Y, XMAX, Y, fill=Scopetube.GRIDCOL, dash=Scopetube.GRIDDASH)

    def sampletime(self):
        return self.smpt
        
    def drawsignals(self):
        p0=None
        for p1 in self.points:
            if p0 is None:
                p0=p1
                continue
            if p1[-1]<self.t0:
                p0=p1
                continue
            self.drawseg(p0, p1)
            p0=p1
    
    def drawseg(self, p0, p1):
        x0=self.getxt(p0[-1])
        x1=self.getxt(p1[-1])
        for i, c, gety, en in zip(range(3), (Scopetube.VCOL, Scopetube.CCOL, Scopetube.PCOL), (self.getyv, self.getyc, self.getyp), self.ena):
            if en: self.create_line(x0, gety(p0[i]), x1, gety(p1[i]), fill=c)

    def load(self,  fname):
        self.resetpoints()
        with open(fname) as f:
            self.points=[]
            l=f.readline()
            while l:
                self.addpoint(tuple([float(v) for v in l.split(',')]))
                l=f.readline()
        print str(self.points)

    def save(self, fname):
        with open(fname, 'w') as f:
            for p in self.points:
                comma=''
                for v in p:
                    f.write(comma)
                    f.write(str(v))
                    comma=','
                f.write('\n')
