# coding: utf-8

"""
DPS supplier memory manager

This windows is used to manage the DPS supplier memories contens. 
DPS has 9 memories (1 to 9) where it stores preset values to be 
quick recalled later. The memory 0 is automatically updated with
the parameters currently in use. From memory windows the memory
can be updated or recalled for review. From the main interface they
can only be recalled. 

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
    """
    Create a wave user interface based on Tkinterface to read and modify the waves to play on the DPS

    """

    def __init__(self, prevroot, datawve):
        """
        Create a waveinterface instance.

        :param prevroot: is the main window 
        :param datawve: is the datapoints to play with
        :returns: a new instance of wave interface

        """    
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
        """
        Update scope and table views
        """     
        self.tablewve.updateview()
        self.scope.redraw()

    def butcmdmodify(self):
        """
        Modify and item of the table.

        Gets the item to modify and new values from the user interface fields.
        """     
        i=self.ivarstep.get()
        if i<len(self.datawve) and i>=0:
            self.datawve[i]=[self.datawve[self.ivarstep.get()][0]]+self.getvc(i)
            self.tablewve.updateview()
            self.scope.redraw()
        else:
            tkMessageBox.showinfo('Step not found', 'Step index is not in the points interval')

    def butcmddelete(self):
        """
        Delete a table row.

        Read the index to delete by the interface field.
        """     
        i=self.ivarstep.get()
        if i<len(self.datawve) and i>=0:        
            del self.datawve[i]
            self.tablewve.updateview()
            self.scope.redraw()
        else:
            tkMessageBox.showinfo('Step not found', 'Step index is not in the points interval')

    def butcmdinsert(self):
        """
        Insert an item on the data table.

        Gets the item data from the interface fields.
        """     
        i=self.tablewve.findtime(self.dvartime.get())
        
        if len(self.datawve)>0 and i>0 and abs(self.datawve[i-1][TPOS]-self.dvartime.get())<0.01:#if the time is the same the insert becomes a modify
            self.datawve[i-1]=[self.dvartime.get()]+self.getvc(i-1)
        else:
            self.datawve.insert(i, [self.dvartime.get()]+self.getvc(i-1))

        self.tablewve.updateview()
        self.scope.redraw()

    def butcmdappend(self):
        """
        Append an item to the data table.

        Gets the item to append values from the user interface fields.
        """
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
        """
        Gets begin data on the clipboard from the first row visible on the data list. 
        """
        r=self.tablewve.getfistvisiblerow()
        self.ivarstep.set(r)
        self.dvartime.set(self.datawve[r][TPOS])
        self.dvarvoltage.set(self.datawve[r][VPOS])
        self.dvarcurrent.set(self.datawve[r][CPOS])

        self.clipboard.setbegin(r)

    def btncmdpckend(self):
        """
        Gets end data on the clipboard from the second row visible on the data list. 
        """
        r=self.tablewve.getfistvisiblerow()+1
        if r<len(self.datawve):
            self.ivarstep.set(r)
            self.dvartime.set(self.datawve[r][TPOS])
            self.dvarvoltage.set(self.datawve[r][VPOS])
            self.dvarcurrent.set(self.datawve[r][CPOS])

            self.clipboard.setend(r)

    def butcmddone(self):
        """
        Close the window.
        """
        self.root.destroy()

    def getvc(self, i):
        """
        Gets voltage and current from the interface fields.
        
        If they are negative, the voltage/current at the given position are taken.
        In case of the first point the value 0 is used.

        :param i: the index from which get parameters if something is < 0
        :return: a list containing voltage and current
        """
        v=self.dvarvoltage.get()
        c=self.dvarcurrent.get()
        
        if i>=0:
            if v<0.: v=self.datawve[i][VPOS]
            if c<0.: c=self.datawve[i][CPOS]
        else:    
            if v<0.: v=0.
            if c<0.: c=0.

        return [v, c]

    def buttoncallback(self, p, action='insert'):
        """
        Insert, modify or delete a point.

        That interface is used by the scopetube to edit the table.
        
        :param p: is a list containing the new value for (t, v, c)
        if v or c are not updated -1 is returned
        :param action: describes the type of action required
        """
        self.dvarvoltage.set(p[1])
        self.dvarcurrent.set(p[2])
        self.dvartime.set(p[0])
        self.ivarstep.set(self.tablewve.findtime(p[0]))
        
        if action == 'insert':
            self.butcmdinsert()
        elif action == 'modify':
            self.butcmdmodify()
        elif action == 'delete':
            self.butcmddelete()
        else:
            print ('Internal error: unexpected button call back in wve interface')

    def btncmdhelp(self):
        """
        Open a window with basic help on the wave interface.
        """
        Txtinterface(self.root, 'Help', 
"""Wave editor window is designed to create new waveform to play on the DPS supplier.
It is based on two output formats:
- top-left is text table showing what happens at voltage and current versus time 
(the step number is showed for edit purpose) 
- bottom-left is graphical and shows the output waveform equivalent to the table
The data can be entered in three ways:
- graphically with mouse clicking on the bottom-left graph
- textually with the commands on top-right 
- from clipboard on bottom-right side
The clipboard can copy/cut and paste from data section. 
Clipboard data can be modified bebore pasting:
- amplified (or attenuated if factor is below 1)
- translated 
- transformed in a ramp
On the graphical section it is possible to manage the enabled waveforms:
- drage with left button pressed to move the waveform(s)
- rotate wheel to zoom/unzoom the time (x)
- press shift while rotating wheel to zoom/unzoom the amplitude (y)
- press ctrl while rotating wheel to change the enabled waveform(s)
- press wheel to fit waveform(s) on x and y scales 
- press right button to insert a point (of enabled variables)
- press shift and right button to modify the amplitude of the point(s) at the right 
of the mouse arrow with mouse amplitude
- press ctrl and right button to delete the point at the right of the mouse pointer
- press ctrl and shift to replace the point at the right of the mouse pointer with the 
current mouse arrow place
On the bottom of the screen the scale, translation and enables are available 
for manual editing
On the top-right side it is possible to add new points:
- insert button adds a new point at given time, use -1 on voltage/current to 
keep previous value
- insert button to insert a new point (with absolute time) if the required time 
is already present, that point is modified with new values
- modify and delete buttons can be used to edit or delete the given step
- append is used to add a new point to the tail of current waaveform known 
the delta time between last one
On the clipboard the time is stored as delta between adiacent points 
while on the main table it is absolute.
On the clipboard are available the following functions:
- Copy and cut from begin/end steps of the data into the clipboard
- Paste clipboard at the given step inserting or overwriteing the data present there
The clipboard can be modified:
- Amplified to stretch in x or y depending on the factors
- Translated on x and y depending on the factors 
- Transform the clipboard in a ramp using first and last points as begin
and end values with given number of steps
The clipboard and the data are showed with following buttons:
- Line up/down to move up or down by 1 line
- Page up/down to move up or dosn by all row available minus 1
- Top/bottom to go to the first or last element
- Goto time/step to move the first line at the given step
- Pick begin/end to read the first/second line and put is in begin/end fields
That is useful for edit purpose without copying by hand
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
