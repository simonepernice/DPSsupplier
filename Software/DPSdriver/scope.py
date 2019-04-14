from Tkinter import Checkbutton, IntVar, DoubleVar, E, W

from scopetube import Scopetube
from gridlayoutrowinsert import insertlabelrow, insertentryrow
from constants import VCOL, CCOL, PCOL

class Scope:        
    def __init__(self, root, data, row0, col0, rowspan=10, colspan=6, showpower=True, horizontaljoin=False, buttoncallback=None):
        self.root=root
        
        row=row0

        rowspan-=4 #those lines are used for inputs

        self.scopetube=Scopetube(root, data, horizontaljoin, self.newratios, buttoncallback)
        self.scopetube.grid(row=row, column=col0, columnspan=colspan, rowspan=rowspan, sticky=E+W)
        
        row+=rowspan
        rowspan=1
        colspan=1
        insertlabelrow(root, row, col0, (("Y [V/div]: ", VCOL), None, ("Y [A/div]: ", CCOL)), E)
        self.dvarvdiv=DoubleVar()
        self.dvarvdiv.set(1.)          
        self.dvarcdiv=DoubleVar()
        self.dvarcdiv.set(1.)        
        entries=insertentryrow(root, row, col0, (None, self.dvarvdiv, None, self.dvarcdiv), 'right', W)
        self.dvarpdiv=DoubleVar()
        self.dvarpdiv.set(1.)                  
        if showpower:
            insertlabelrow(root, row, col0, (None, None, None, None, ("Y [W/div]: ", PCOL)), E)
            entries+=insertentryrow(root, row, col0, (None, None, None, None, None, self.dvarpdiv), 'right', W)
        
        row+=rowspan
        insertlabelrow(root, row, col0, (("Y0 [V]: ", VCOL), None, ("Y0 [A]: ", CCOL)), E)
        self.dvarv0=DoubleVar()
        self.dvarv0.set(0.)          
        self.dvarc0=DoubleVar()
        self.dvarc0.set(0.)        
        entries+=insertentryrow(root, row, col0, (None, self.dvarv0, None, self.dvarc0), 'right', W)        
        self.dvarp0=DoubleVar()
        self.dvarp0.set(0.) 
        if showpower:
            insertlabelrow(root, row, col0, (None, None, None, None, ("Y0 [W]: ", PCOL)), E)
            entries+=insertentryrow(root, row, col0, (None, None, None, None, None, self.dvarp0), 'right', W)

        row+=rowspan
        rowspan=1
        colspan=2
        col=col0
        self.ivarvena=IntVar()
        self.ivarvena.set(1)        
        Checkbutton(root, variable=self.ivarvena, text='Voltage show', foreground=VCOL, command=self.entbndcmdbutscpupdt).grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        col+=colspan
        self.ivarcena=IntVar()
        self.ivarcena.set(1)        
        Checkbutton(root, variable=self.ivarcena, text='Current show', foreground=CCOL, command=self.entbndcmdbutscpupdt).grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        self.ivarpena=IntVar()
        self.ivarpena.set(0)
        if showpower:
            col+=colspan
            self.ivarpena.set(1)
            Checkbutton(root, variable=self.ivarpena, text='Power show', foreground=PCOL, command=self.entbndcmdbutscpupdt).grid(row=row, column=col, columnspan=colspan, sticky=E+W)

        row+=rowspan
        col=col0
        insertlabelrow(root, row, col0, ("X [s/div]: ", None, "X0 [s]: "), E)
        self.dvartdiv=DoubleVar()
        self.dvartdiv.set(60.)        
        self.dvart0=DoubleVar()
        self.dvart0.set(0.)        
        entries+=insertentryrow(root, row, col0, (None, self.dvartdiv, None, self.dvart0), 'right', W)

        for e in entries:
            e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
            e.bind('<Return>', self.entbndcmdbutscpupdt)

        self.varlist=(self.ivarvena, self.ivarcena, self.ivarpena, self.dvarvdiv, self.dvarcdiv, self.dvarpdiv, self.dvarv0, self.dvarc0, self.dvarp0, self.dvartdiv, self.dvart0)

        self.update()
#        self.scopetube.update()
#        self.entbndcmdbutscpupdt(None)

    def entbndcmdbutscpupdt(self,  *event):
        self.scopetube.setratios([e.get() for e in self.varlist])
        self.scopetube.redraw()

    def newratios(self, ratios):
        for var, val in zip(self.varlist, ratios):
            var.set(val)

    def update(self):
        self.scopetube.update()
        self.entbndcmdbutscpupdt(None)

    def resetpoints(self):
        self.scopetube.resetpoints()
    
    def addpoint(self, p):
        self.scopetube.addpoint(p)
        
    def redraw(self):
        self.scopetube.redraw()

#    def drawgrid(self):
#        self.scopetube.drawgrid()

    def sampletime(self):
        return self.scopetube.sampletime()

    def load(self,  fname):
        self.scopetube.load(fname)

    def save(self, fname):
        self.scopetube.save(fname)

if __name__=='__main__':
    from Tkinter import Tk
    root=Tk()

    scope=Scope(root, [], 0, 0)
    
    scope.load('../tests/testpoints.dps')
    scope.redraw()
    root.mainloop()
        


