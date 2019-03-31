from Tkinter import Button, IntVar, DoubleVar, E, W, N, S
from ttk import Separator
import tkMessageBox

from constants import TABLEROW, TABLECOL, VCOL, CCOL, TPOS, VPOS, CPOS
from clipboard import Clipboard
from table import Table
from scope import Scope
from gridlayoutrowinsert import insertlabelrow, insertentryrow

class Wveinterface:        

    def __init__(self, root, datawve):    
        self.root=root
        self.root.title("Wave editor")
        
        self.datawve=datawve

        self.dataclpbrd=[]
        self.clipboardtime=0

        row=0
        col=0        
        self.tablewve=Table(root, self.datawve, ('step', 'time [s]', ('voltage [V]', VCOL), ('current [A]', CCOL)), row, col, TABLEROW, TABLECOL)
        
        SCOPEROWSPAN=15
        self.scope=Scope(root, self.datawve, TABLEROW+1+1, 0, rowspan=SCOPEROWSPAN, showpower=False, horizontaljoin=True)
        
        row=1
        rowspan=1
        colspan=1
        col=TABLECOL+colspan
        Button(root, text="Pick beg", command=self.btncmdpckbeg).grid(row=row, column=col, sticky=E+W, padx=8)
        col=TABLECOL+colspan        
        row+=rowspan
        Button(root, text="Pick end", command=self.btncmdpckend).grid(row=row, column=col, sticky=E+W, padx=8)

        Separator(root, orient='horizontal').grid(row=TABLEROW+1, column=0, columnspan=TABLECOL+2+1+6, sticky=E+W, pady=8)
        
        Separator(root, orient='vertical').grid(row=0, column=6, rowspan=1+TABLEROW+1+SCOPEROWSPAN, sticky=N+S, padx=8)        

        row=0
        COL1=TABLECOL+2+1
        col=COL1
        colspan=1
        insertlabelrow(root, row, col, (None, None, ('voltage [V]', VCOL), ('current [A]', CCOL))) 

        row+=rowspan
        insertlabelrow(root, row, col, ('time [s]:', )) 
        self.dvartime=DoubleVar()
        self.dvarvoltage=DoubleVar()
        self.dvarcurrent=DoubleVar()
        insertentryrow(root, row, col, (None, self.dvartime, self.dvarvoltage, self.dvarcurrent)) 
        col+=TABLECOL
        Button(root, text="Insert", command=self.butcmdinsert).grid(row=row, column=col, sticky=E+W, padx=8)

        row+=rowspan
        col=COL1
        insertlabelrow(root, row, col, ('step :', )) 
        self.ivarstep=IntVar()
        insertentryrow(root, row, col, (None, self.ivarstep, self.dvarvoltage, self.dvarcurrent)) 
        col+=TABLECOL
        Button(root, text="Modify", command=self.butcmdmodify).grid(row=row, column=col, sticky=E+W, padx=8)
        col+=colspan
        Button(root, text="Delete", command=self.butcmddelete).grid(row=row, column=col, sticky=E+W, padx=8)

        row+=rowspan
        col=COL1
        insertlabelrow(root, row, col, ('pause [s]:', ))        
        self.dvarpause=DoubleVar()
        insertentryrow(root, row, col, (None, self.dvarpause, self.dvarvoltage, self.dvarcurrent)) 
        col+=TABLECOL
        Button(root, text="Append", command=self.butcmdappend).grid(row=row, column=col, sticky=E+W, padx=8)

        self.clipboard=Clipboard(root, self.datawve, self.updateview, TABLEROW+2, COL1)
        

        col=COL1+TABLECOL+1
        colspan=1
        row=TABLEROW+1+SCOPEROWSPAN
        Button(root, text="Done", command=self.butcmddone).grid(row=row, column=col, sticky=E+W, padx=8)

        self.scope.update()
        self.scope.redraw()

    def updateview(self):
        self.tablewve.updateview()
        self.scope.redraw()

    def butcmdmodify(self):
        i=self.ivarstep.get()
        if i>=len(self.datawve) or i<0:
            self.datawve[i]=[self.datawve[self.ivarstep.get()][0], self.dvarvoltage.get(), self.dvarcurrent.get()]
            self.tablewve.updateview()
            self.scope.redraw()
        else:
            tkMessageBox.showinfo('Step not found', 'Step index is not in the points interval')

    def butcmddelete(self):
        i=self.ivarstep.get()
        if i>=len(self.datawve) or i<0:        
            del self.datawve[i]
            self.tablewve.updateview()
            self.scope.redraw()
        else:
            tkMessageBox.showinfo('Step not found', 'Step index is not in the points interval')

    def butcmdinsert(self):
        i=self.tablewve.findtime(self.dvartime.get())
        if len(self.datawve)>0 and i>0 and abs(self.datawve[i-1][TPOS]-self.dvartime.get())<0.01:#if the time is the same the insert becomes a modify
            self.datawve[i-1]=[self.dvartime.get(), self.dvarvoltage.get(), self.dvarcurrent.get()]
        else:
            self.datawve.insert(i,[self.dvartime.get(), self.dvarvoltage.get(), self.dvarcurrent.get()])
        self.tablewve.updateview()
        self.scope.redraw()

    def butcmdappend(self):
        if self.dvarpause.get()<=0:
            tkMessageBox.showinfo('Time not monotonic', 'Time pause has to be > 0')
            return

        if len(self.datawve)>0:
            t0=self.datawve[-1][TPOS]
        else:
            t0=0

        self.datawve.append([self.dvarpause.get()+t0, self.dvarvoltage.get(), self.dvarcurrent.get()])
        self.tablewve.updateview()
        self.scope.redraw()
        
    def btncmdpckbeg(self):
        r=self.tablewve.getfistvisiblerow()
        self.ivarstep.set(r)
        self.dvartime.set(self.datawve[r][TPOS])
        self.dvarvoltage.set(self.datawve[r][VPOS])
        self.dvarcurrent.set(self.datawve[r][CPOS])

        self.clipboard.setbegin(r)

    def btncmdpckend(self):
        r=self.tablewve.getfistvisiblerow()+1
        if r<len(self.datawve):
            self.ivarstep.set(r)
            self.dvartime.set(self.datawve[r][TPOS])
            self.dvarvoltage.set(self.datawve[r][VPOS])
            self.dvarcurrent.set(self.datawve[r][CPOS])

            self.clipboard.setend(r)

    def butcmddone(self):
        self.root.destroy()

if __name__=='__main__':
    from Tkinter import Tk
    from dpsfile import Dpsfile
    root=Tk()
    points=[]
    for r in range(1,35):
        line=[]
        for c in range(3):
            line.append(r*10+1.11*(c+1))
        points.append(line)
            
    my_gui=Wveinterface(root, Dpsfile(points))
    root.mainloop()
