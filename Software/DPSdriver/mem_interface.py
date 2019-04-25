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

from constants import VCOL, CCOL, PCOL
from gridlayoutrowinsert import insertlabelrow, insertentryrow
from toplevel import maketoplevel
from txtinterface import Txtinterface

try:
    from Tkinter import Label, Button, Checkbutton, Scale, IntVar, DoubleVar, E, W
except ImportError:
    from tkinter import Label, Button, Checkbutton, Scale, IntVar, DoubleVar, E, W

__author__ = "Simone Pernice"
__copyright__ = "Copyright 2019, DPS supplier"
__credits__ = ["Simone Pernice"]
__license__ = "GNU GPL v3.0"
__version__ = "0.9.0"
__date__ = "16 April 2019"
__maintainer__ = "Simone Pernice"
__email__ = "perniceb@libero.it"
__status__ = "Development"

class Meminterface:
    """
    Create a memory window user interface based on Tkinterface to read and modify the DPS memories

    """

    def __init__(self, prevroot, dps, updatefields):
        """
        Create a memory interface.

        :param prevroot: is the main window 
        :param dps: is the dps class instance used to read/write the memory 
        :param updatefields: is used to update the fields showed by the main interface if something changed
        :returns: a new instance of memory interface

        """
        self.root=maketoplevel(prevroot, True)
        self.root.title("Memory editor")
        
        self.dps=dps
        self.updatefields=updatefields

        row=0
        col=0
        colspan=2
        rowspan=1
        self.ivarmem=IntVar()
        Scale(self.root, label='Memory', variable=self.ivarmem, from_=0, to=9, resolution=1, orient="horizontal").grid(row=row, column=col, sticky=W+E, columnspan=colspan)
        col+=colspan
        Button(self.root, text="Recall", command=self.butcmdrecall).grid(row=row, column=col, columnspan=colspan, sticky=E+W, padx=8)
        col+=colspan
        Button(self.root, text='Store', command=self.butcmdstore).grid(row=row, column=col, columnspan=colspan, sticky=E+W, padx=8)     

        colspan=1
        row+=rowspan        
        col=0
       
        insertlabelrow(self.root, row, col, (("Vset [V]: ", VCOL), None, ("Cset [A]: ", CCOL)), E)
        self.dvarvset=DoubleVar()
        self.dvarcset=DoubleVar()
        insertentryrow(self.root, row, col, (None, self.dvarvset, None, self.dvarcset), 'right', W)

        colspan=1
        row+=rowspan
        col=0

        insertlabelrow(self.root, row, col, (("Vmax [V]: ", VCOL), None, ("Cmax [A]: ", CCOL), None, ("Pmax [W]: ", PCOL)), E)
        self.dvarvmax=DoubleVar()
        self.dvarcmax=DoubleVar()
        self.dvarpmax=DoubleVar()
        insertentryrow(self.root, row, col, (None, self.dvarvmax, None, self.dvarcmax, None, self.dvarpmax), 'right', W)

        row+=rowspan
        colspan=1
        col=0
        Label(self.root, text='Bright:').grid(row=row, column=col, columnspan=colspan)
        col+=colspan      
        self.ivarbrght=IntVar()
        Scale(self.root, variable=self.ivarbrght, from_=0, to=5, resolution=1, orient="horizontal").grid(row=row, column=col, columnspan=colspan)#, label='Brightness'
        col+=colspan
        colspan=2
        self.ivaroutmset=IntVar()
        self.ivaroutmset.set(0)
        Checkbutton(self.root, variable=self.ivaroutmset, text="Out same/off@MSet").grid(row=row, column=col, sticky=E+W, columnspan=colspan)
        col+=colspan
        self.ivaroutpwron=IntVar()
        self.ivaroutpwron.set(0)
        Checkbutton(self.root, variable=self.ivaroutpwron, text="Out on/off@PwOn").grid(row=row, column=col, sticky=E+W, columnspan=colspan)

        row+=rowspan
        colspan=2
        col=2
        Button(self.root, text="Help", command=self.btncmdhelp).grid(row=row, column=col, sticky=E+W, columnspan=colspan, padx=8)
        col+=colspan
        Button(self.root, text="Done", command=self.btncmddone).grid(row=row, column=col, sticky=E+W, columnspan=colspan, padx=8)

    def memregs(self):
        """
        Build the list to recall all memory attributes for the user register set

        :returns: the list to recall the currently selected memory attribute
        """
        mem='m'+str(self.ivarmem.get())
        return [mem+a for a in ['vset', 'cset',  'ovp', 'ocp', 'opp', 'brght', 'pre', 'onoff']]

    def butcmdrecall(self):
        """
        Recall all the currently selected memory parameters setting the interface accordingly
        """
        mr=self.memregs()
        data=self.dps.get(mr)
        self.dvarvset.set(data[0])
        self.dvarcset.set(data[1])
        self.dvarvmax.set(data[2])
        self.dvarcmax.set(data[3])
        self.dvarpmax.set(data[4])
        self.ivarbrght.set(data[5])
        self.ivaroutmset.set(data[6])
        self.ivaroutpwron.set(data[7])
    
    def butcmdstore(self):
        """
        Store in the currently selected memory all the parameters set in the interface
        If the memory 0 (currently in use) is modified also dps main interface is updated
        """
        mr=self.memregs()
        mv=[
            self.dvarvset.get(), 
            self.dvarcset.get(), 
            self.dvarvmax.get(), 
            self.dvarcmax.get(), 
            self.dvarpmax.get(), 
            self.ivarbrght.get(), 
            self.ivaroutmset.get(), 
            self.ivaroutpwron.get()
        ]
        self.dps.set(mr, mv)
        if self.ivarmem.get()==0:
            self.updatefields(True)

    def btncmdhelp(self):
        """
        Provides basic help on memory window usage.
        """
        Txtinterface(self.root, 'Memory help', 
"""The DPS supplier has 10 memories: 0 to 9. 
On each memory is possible to set: 
- output voltage and current; 
- maximum voltage, current and power; 
- brightness; 
- output status at memory recall and at power on.
The memory 0 should not used. It stores the current DPS 
status and therefore it is automatically updated  by DPS 
with the configuration currenty in use (or the recall memory).
This interface is for recall and store the memories settings. 
From the main interface it is possible to recall memories 
from 1 to 9 .""")

    def btncmddone(self):
        """
        Close the memory window
        """    
        self.root.destroy()

if __name__=='__main__':
    try:
        from Tkinter import Tk
    except ImportError:
        from tkinter import Tk

    root=Tk()
    my_gui=Meminterface(root,  None,  None)
    root.mainloop()
