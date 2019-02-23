from Tkinter import Canvas, ALL

class Scopetube(Canvas):
    XDIV=10.
    YDIV=8.
    GRIDDASH=(1, 6)
    GRIDCOL='black'
    VCOL='red'
    CCOL='blue'
    MINSAMPLETIME=1.
    
    def __init__(self, root):
        Canvas.__init__(self, root, background='white')
        
        self.resetpoints()
                
    def setratios(self, vdiv,  cdiv,  tdiv, t0):
        self.vm=-self.winfo_height()/Scopetube.YDIV/vdiv
        self.vq=self.winfo_height()
        self.vdiv=vdiv
        self.cm=-self.winfo_height()/Scopetube.YDIV/cdiv
        self.cq=self.winfo_height()      
        self.tm=self.winfo_width()/Scopetube.XDIV/tdiv
        self.t0=t0
        self.tdiv=tdiv
        self.smpt=1./self.tm
        if self.smpt<Scopetube.MINSAMPLETIME:
            self.smpt=Scopetube.MINSAMPLETIME        

    def getyv(self,  v):
        return v*self.vm+self.vq

    def getyc(self,  c):
        return c*self.cm+self.cq

    def getxt(self,  t):
        return (t-self.t0)*self.tm

    def resetpoints(self):
        self.points=[]
    
    #a point is made by: (voltage, current, time)
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
            if p1[2]<self.t0:
                p0=p1
                continue
            self.drawseg(p0, p1)
            p0=p1
    
    def drawseg(self, p0, p1):
        x0=self.getxt(p0[2])
        x1=self.getxt(p1[2])
        self.create_line(x0, self.getyv(p0[0]), x1, self.getyv(p1[0]), fill=Scopetube.VCOL)
        self.create_line(x0, self.getyc(p0[1]), x1, self.getyc(p1[1]), fill=Scopetube.CCOL)
