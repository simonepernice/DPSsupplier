from Tkinter import Canvas, ALL

class Scopetube(Canvas):
    XDIV=10.
    YDIV=8.
    GRIDDASH=(1, 6)
    GRIDCOL='black'
    VCOL='red'
    CCOL='blue'
    
    def __init__(self, root):
        Canvas.__init__(self, root, background='white')
        
        self.resetpoints()
                
    def setvdiv(self, vdiv):
        self.vm=-self.winfo_height()/Scopetube.YDIV/vdiv
        self.vq=self.winfo_height()

    def getyv(self,  v):
        return v*self.vm+self.vq

    def setcdiv(self, cdiv):
        self.cm=-self.winfo_height()/Scopetube.YDIV/cdiv
        self.cq=self.winfo_height()

    def getyc(self,  c):
        return c*self.cm+self.cq

    def settdiv(self, tdiv, t0):
        self.tm=self.winfo_width()/Scopetube.XDIV/tdiv
        self.t0=t0
    
    def getx(self,  t):
        return (t-self.t0)*self.tm

    def resetpoints(self):
        self.points=[]
    
    #a point is made by: (voltage, current, time)
    def addpoint(self, p):
        self.points.append(p)
        if len(self.points)>2:
            self.drawseg(self.points[-2], self.points[-1])
        
    def clearscreen(self):
        self.delete(ALL)
        self.drawgrid()
        self.drawsignals()

    def drawgrid(self):
        H=self.winfo_height()
        W=self.winfo_width()
        for x in range(0, W, int(W/(Scopetube.XDIV+1))):
            self.create_line(x, 0, x, H, fill=Scopetube.GRIDCOL, dash=Scopetube.GRIDDASH)
            
        for y in range(0, H, int(H/(Scopetube.YDIV+1))):
            self.create_line(0, y, W, y, fill=Scopetube.GRIDCOL, dash=Scopetube.GRIDDASH)

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
    
    def drawseg(self, p0, p1):
        x0=self.getx(p0[2])
        x1=self.getx(p1[2])
        self.create_line(x0, self.getyv(p0[0]), x1, self.getyv(p1[0]), fill=Scopetube.VCOL)
        self.create_line(x0, self.getyc(p0[1]), x1, self.getyc(p1[1]), fill=Scopetube.CCOL)
