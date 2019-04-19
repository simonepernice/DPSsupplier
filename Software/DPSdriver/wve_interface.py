from constants import TABLEROW, TABLECOL, VCOL, CCOL, TPOS, VPOS, CPOS
from clipboard import Clipboard
from table import Table
from scope import Scope
from gridlayoutrowinsert import insertlabelrow, insertentryrow
from txtinterface import Txtinterface
from toplevel import maketoplevel

try:
    from Tkinter import Button, IntVar, DoubleVar, E, W, N, S
    from ttk import Separator
    import tkMessageBox
except ImportError:
    from tkinter import Button, IntVar, DoubleVar, E, W, N, S
    from tkinter.ttk import Separator
    from tkinter import messagebox as tkMessageBox

class Wveinterface:        

    def __init__(self, prevroot, datawve):    
        self.root=maketoplevel(prevroot, True)
        self.root.title("Wave editor")
        
        self.datawve=datawve

        self.dataclpbrd=[]
        self.clipboardtime=0

        row=0
        col=0        
        self.tablewve=Table(self.root, self.datawve, ('step', 'time [s]', ('voltage [V]', VCOL), ('current [A]', CCOL)), row, col, TABLEROW, TABLECOL)
        
        SCOPEROWSPAN=15
        self.scope=Scope(self.root, self.datawve, TABLEROW+1+1, 0, rowspan=SCOPEROWSPAN, showpower=False, horizontaljoin=True, buttoncallback=self.buttoncallback)
        
        row=1
        rowspan=1
        colspan=1
        col=TABLECOL+colspan
        Button(self.root, text="Pick beg", command=self.btncmdpckbeg).grid(row=row, column=col, sticky=E+W, padx=8)
        col=TABLECOL+colspan        
        row+=rowspan
        Button(self.root, text="Pick end", command=self.btncmdpckend).grid(row=row, column=col, sticky=E+W, padx=8)

        Separator(self.root, orient='horizontal').grid(row=TABLEROW+1, column=0, columnspan=TABLECOL+2+1+6, sticky=E+W, pady=8)
        
        Separator(self.root, orient='vertical').grid(row=0, column=6, rowspan=1+TABLEROW+1+SCOPEROWSPAN, sticky=N+S, padx=8)        

        row=0
        COL1=TABLECOL+2+1
        col=COL1
        colspan=1
        insertlabelrow(self.root, row, col, (None, None, ('voltage [V]', VCOL), ('current [A]', CCOL))) 

        row+=rowspan
        insertlabelrow(self.root, row, col, ('time [s]:', )) 
        self.dvartime=DoubleVar()
        self.dvarvoltage=DoubleVar()
        self.dvarcurrent=DoubleVar()
        insertentryrow(self.root, row, col, (None, self.dvartime, self.dvarvoltage, self.dvarcurrent)) 
        col+=TABLECOL
        Button(self.root, text="Insert", command=self.butcmdinsert).grid(row=row, column=col, sticky=E+W, padx=8)

        row+=rowspan
        col=COL1
        insertlabelrow(self.root, row, col, ('step :', )) 
        self.ivarstep=IntVar()
        insertentryrow(self.root, row, col, (None, self.ivarstep, self.dvarvoltage, self.dvarcurrent)) 
        col+=TABLECOL
        Button(self.root, text="Modify", command=self.butcmdmodify).grid(row=row, column=col, sticky=E+W, padx=8)
        col+=colspan
        Button(self.root, text="Delete", command=self.butcmddelete).grid(row=row, column=col, sticky=E+W, padx=8)

        row+=rowspan
        col=COL1
        insertlabelrow(self.root, row, col, ('pause [s]:', ))        
        self.dvarpause=DoubleVar()
        insertentryrow(self.root, row, col, (None, self.dvarpause, self.dvarvoltage, self.dvarcurrent)) 
        col+=TABLECOL
        Button(self.root, text="Append", command=self.butcmdappend).grid(row=row, column=col, sticky=E+W, padx=8)

        self.clipboard=Clipboard(self.root, self.datawve, self.updateview, TABLEROW+2, COL1)
        

        col=COL1+TABLECOL
        colspan=1
        row=TABLEROW+1+SCOPEROWSPAN
        Button(self.root, text="Help", command=self.btncmdhelp).grid(row=row, column=col, sticky=E+W, padx=8)
        col+=1
        Button(self.root, text="Done", command=self.butcmddone).grid(row=row, column=col, sticky=E+W, padx=8)

        self.scope.update()
        self.scope.redraw()

    def updateview(self):
        self.tablewve.updateview()
        self.scope.redraw()

    def butcmdmodify(self):
        i=self.ivarstep.get()
        if i<len(self.datawve) and i>0:
            self.datawve[i]=[self.datawve[self.ivarstep.get()][0]]+self.getvc(i)
            self.tablewve.updateview()
            self.scope.redraw()
        else:
            tkMessageBox.showinfo('Step not found', 'Step index is not in the points interval')

    def butcmddelete(self):
        i=self.ivarstep.get()
        if i<len(self.datawve) or i>=0:        
            del self.datawve[i]
            self.tablewve.updateview()
            self.scope.redraw()
        else:
            tkMessageBox.showinfo('Step not found', 'Step index is not in the points interval')

    def butcmdinsert(self):
        i=self.tablewve.findtime(self.dvartime.get())
        
        if len(self.datawve)>0 and i>0 and abs(self.datawve[i-1][TPOS]-self.dvartime.get())<0.01:#if the time is the same the insert becomes a modify
            self.datawve[i-1]=[self.dvartime.get()]+self.getvc(i-1)
        else:
            self.datawve.insert(i, [self.dvartime.get()]+self.getvc(i-1))

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

        self.datawve.append([self.dvarpause.get()+t0]+self.getvc(len(self.datawve)-1))
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

    def getvc(self, i):
        v=self.dvarvoltage.get()
        c=self.dvarcurrent.get()
        
        if i>=0:
            if v<0: v=self.datawve[i][VPOS]
            if c<0: c=self.datawve[i][CPOS]
        else:    
            if v<0: v=0
            if c<0: c=0

        return [v, c]

    def buttoncallback(self, p):
        self.dvartime.set(p[0])
        self.dvarvoltage.set(p[1])
        self.dvarcurrent.set(p[2])
        self.butcmdinsert()

    def btncmdhelp(self):
        Txtinterface(self.root, 'Help', 
"""Wave editor window is designed to create new waveform to play on the DPS supplier.
It is based on two output formats:
- top-left is text table showing what happens at voltage and current versus time (step is showed for edit purpose) 
- bottom-left is graphical and shows the output waveform equivalent to the table above
The data can be entered in three ways:
- graphically clicking with right button on the bottom-left graph
- textually with the commands on top-right 
- from clipboard on bottom-right side
The clipboard can copy/cut and paste from data section. 
Clipboard data can be modified bebore pasting:
- amplified (or attenuated if factor is below 1)
- translated 
- transformed in a ramp
On the graphical section it is possible to manage the waveforms:
- the following mouse actions works only on enabled waveforms
- drage with right button pressed to move the waveform(s)
- rotate wheel to zoom the time (x)
- press shift while rotating wheel to zoom y
- press ctrs while rotating wheel to change the enabled waveform(s)
- press wheel to fit x and y scale
On the bottom of the screen the scale, translation and enables are available for manual editing
On the top-right side it is possible to add new points:
- insert button adds a new point at given time, use -1 on voltage/current to keep previous value
- insert button with time already present modifies it
- modify and delete buttons can be used to edit or delete the given step
- append is used to add a new point to the tail of current waaveform known the delta time between last one
On the clipboard the time on the clipboard is stored as delta between adiacent points while on the main table it is absolute.
On the clipboard are available the following buttons:
- Copy and past from begin/end steps
- Amplify or translate the clipboard
- Transform the clipboard in a ramp using first and last points with given number of steps
- Paste clipboard at the diven step inserting or overwriteing the data present there
The clipboard and the data are showed in table with following functions:
- Line up/down to move up or down by 1 line
- Page up/down to move up or dosn by all row available minus 1
- Top/bottom to go to the first or last element
- Goto time/step to move the first line at the given step
- Pick begin/end to read the first/second line and put is in begin/end fields
""")         

if __name__=='__main__':
    try:
        from Tkinter import Tk
    except ImportError:
        from tkinter import Tk

    root=Tk()
    points=[]
    for r in range(1,35):
        line=[]
        for c in range(3):
            line.append(r*10+1.11*(c+1))
        points.append(line)
            
    my_gui=Wveinterface(root, points)
    root.mainloop()
