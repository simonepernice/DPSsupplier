from Tkinter import Label, Checkbutton, Entry, IntVar, DoubleVar, E, W

from scopetube import Scopetube

from constants import ENTRYWIDTH, VCOL, CCOL, PCOL

class Scope:        
    def __init__(self, root, data, row0, col0, rowspan=10, colspan=6):
        self.root=root
        
        row=row0
        col=col0
        rowspan-=4 #those lines are used for inputs
        
#        rowspan=1
#        colspan=1
#        Label(root, text="Vout [V]: ", foreground=VCOL).grid(row=row, column=col, sticky=E)
#        col+=colspan
#        self.dvarvout=DoubleVar()
#        Entry(root, textvariable=self.dvarvout, state='readonly', width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)
#        col+=colspan
#        Label(root, text="Cout [A]: ", foreground=CCOL).grid(row=row, column=col, sticky=E)
#        col+=colspan
#        self.dvarcout=DoubleVar()
#        Entry(root, textvariable=self.dvarcout, state='readonly', width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)
#        col+=colspan
#        Label(root, text="Pout [W]: ", foreground=PCOL).grid(row=row, column=col, sticky=E)
#        col+=colspan
#        self.dvarpout=DoubleVar()
#        Entry(root, textvariable=self.dvarpout, state='readonly', width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)        

#        row+=rowspan
#        col=col0
 
        self.scopetube=Scopetube(root, data)
        self.scopetube.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan, sticky=E+W)
        
        row+=rowspan
        rowspan=1
        colspan=1
        col=col0
        Label(root, text="Y [V/div]: ", foreground=VCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvdiv=DoubleVar()
        self.dvarvdiv.set(1.)          
        e=Entry(root, textvariable=self.dvarvdiv, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
        e.bind('<Return>', self.entbndcmdbutscpupdt)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Y [A/div]: ", foreground=CCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarcdiv=DoubleVar()
        self.dvarcdiv.set(1.)        
        e=Entry(root, textvariable=self.dvarcdiv, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
        e.bind('<Return>', self.entbndcmdbutscpupdt)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Y [W/div]: ", foreground=PCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarpdiv=DoubleVar()
        self.dvarpdiv.set(1.)          
        e=Entry(root, textvariable=self.dvarpdiv, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
        e.bind('<Return>', self.entbndcmdbutscpupdt)
        e.grid(row=row, column=col, sticky=W)

        row+=rowspan
        rowspan=1
        colspan=1
        col=col0 
        Label(root, text="Y0 [V]: ", foreground=VCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarv0=DoubleVar()
        self.dvarv0.set(0.)          
        e=Entry(root, textvariable=self.dvarv0, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
        e.bind('<Return>', self.entbndcmdbutscpupdt)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Y0 [A]: ", foreground=CCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarc0=DoubleVar()
        self.dvarc0.set(0.)        
        e=Entry(root, textvariable=self.dvarc0, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
        e.bind('<Return>', self.entbndcmdbutscpupdt)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Y0 [W]: ", foreground=PCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarp0=DoubleVar()
        self.dvarp0.set(0.)          
        e=Entry(root, textvariable=self.dvarp0, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
        e.bind('<Return>', self.entbndcmdbutscpupdt)
        e.grid(row=row, column=col, sticky=W)

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
        col+=colspan
        self.ivarpena=IntVar()
        self.ivarpena.set(1)        
        Checkbutton(root, variable=self.ivarpena, text='Power show', foreground=PCOL, command=self.entbndcmdbutscpupdt).grid(row=row, column=col, columnspan=colspan, sticky=E+W)

        row+=rowspan
        col=col0
        colspan=1
        rowspan=1
        Label(root, text="X [s/div]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarsdiv=DoubleVar()
        self.dvarsdiv.set(60.)        
        e=Entry(root, textvariable=self.dvarsdiv, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
        e.bind('<Return>', self.entbndcmdbutscpupdt)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan        
        Label(root, text="X0 [s]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvars0=DoubleVar()
        self.dvars0.set(0.)        
        e=Entry(root, textvariable=self.dvars0, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
        e.bind('<Return>', self.entbndcmdbutscpupdt)
        e.grid(row=row, column=col, sticky=W)        
#        col+=colspan
#        Label(root, text="S.Rate[s/Sa]: ").grid(row=row, column=col, sticky=E)
#        col+=colspan
#        self.dvarsecsmp=DoubleVar()        
#        e=Entry(root, textvariable=self.dvarsecsmp, width=ENTRYWIDTH, justify='right')
#        e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
#        e.bind('<Return>', self.entbndcmdbutscpupdt)
#        e.grid(row=row, column=col, sticky=W)            

        self.scopetube.update()
        self.entbndcmdbutscpupdt(None) 
#        self.dvarsecsmp.set(round(self.scopetube.sampletime(), 1))

    def entbndcmdbutscpupdt(self,  *event):
        self.scopetube.setratios(
            self.dvarvdiv.get(), self.dvarv0.get(), self.ivarvena.get(),
            self.dvarcdiv.get(), self.dvarc0.get(), self.ivarcena.get(),  
            self.dvarpdiv.get(), self.dvarp0.get(), self.ivarpena.get(),  
            self.dvarsdiv.get(), self.dvars0.get()
        )
        self.scopetube.redraw()
        
#    def getsecsmp(self):
#        return self.dvarsecsmp.get()

    def update(self):
        self.scopetube.update()

    def resetpoints(self):
        self.scopetube.resetpoints()
    
    #a point is made by: (time, voltage, current, power)
    def addpoint(self, p):
#        self.dvarvout.set(p[1])
#        self.dvarcout.set(p[2])
#        self.dvarpout.set(p[3])
        self.scopetube.addpoint(p)
        
    def redraw(self):
        self.scopetube.redraw()

    def drawgrid(self):
        self.scopetube.drawgrid()

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
    root.mainloop()
        


