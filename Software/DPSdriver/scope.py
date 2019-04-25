# coding: utf-8

"""
DPS scope

This is the DPS scope interface with settings regulations.
It is used to display polling wave on DPS output or 
to edit a waveform.

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

from scopetube import Scopetube
from gridlayoutrowinsert import insertlabelrow, insertentryrow
from constants import VCOL, CCOL, PCOL

try:
    from Tkinter import Checkbutton, IntVar, DoubleVar, E, W
except ImportError:
    from tkinter import Checkbutton, IntVar, DoubleVar, E, W

__author__ = "Simone Pernice"
__copyright__ = "Copyright 2019, DPS supplier"
__credits__ = ["Simone Pernice"]
__license__ = "GNU GPL v3.0"
__version__ = "0.9.0"
__date__ = "16 April 2019"
__maintainer__ = "Simone Pernice"
__email__ = "perniceb@libero.it"
__status__ = "Development"

class Scope:

    """
    Scope is class used to make a scope on grid layout with Tkinterface.

    """
    def __init__(self, root, data, row0, col0, rowspan=10, colspan=6, showpower=True, horizontaljoin=False, buttoncallback=None):
        """
        Create a scope interface.

        :param root: is the main window
        :param data: is the data to display (update if enabled)
        :param row0: is the beginning row as whitch the scope should be placed on the grid layout
        :param col0: is the beginning column as whitch the scope should be placed on the grid layout
        :param rowspan: is how many rows should be used to draw the whole scope
        :param colspan: is how many columns should be used to draw the whole scope
        :param showpower: is a boolean field used to show the power (not required in wave editor) 
        :param horizontaljoin: if true the points are joined through horizontal segments then vertica 
        (for waveditor) if it is false they are just joined as useful in the scope view
        :param buttoncallback: it is the function to provide if the user can manage the graphs 
        changing point (for wave editor)
        :returns: a new instance of scope

        """    
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

    def entbndcmdbutscpupdt(self,  *event):
        """
        Updates scope view ratios when something changes on any of the setting.
        
        The change is detected by RETURN pressure or field change

        :param event: may the event that made the change (not used), added to be used as command/event call back

        """        
        self.scopetube.setratios([e.get() for e in self.varlist])
        self.scopetube.redraw()

    def newratios(self, ratios):
        """
        Updates scope ratios.
        
        Used by scopetube to update the ratios base on the mouse actions.

        :param ratios: is the list of ratios to update: v, c, p enables; v, c, p initial value; v, c, p divisions; t initial value and divisions.

        """     
        for var, val in zip(self.varlist, ratios):
            var.set(val)

    def update(self):
        """
        Updates scope tube view based on the dimensions of the screen.
        
        """    
        self.scopetube.update()
        self.entbndcmdbutscpupdt(None)

    def resetpoints(self):
        """
        Delete all the waveform points .
        
        """   
        self.scopetube.resetpoints()
    
    def addpoint(self, p):
        """
        Add a new point to the waveform.
        
        """
        self.scopetube.addpoint(p)
        
    def redraw(self):
        """
        Redraw the scopetube.
        
        """       
        self.scopetube.redraw()

    def sampletime(self):
        """
        Gets the scopetube suggested sample time. 
        
        That is the sample time required to have a sample for every pixel.
        
        """       
        return self.scopetube.sampletime()

    def load(self,  fname):
        """
        Load a waveform saved before (uses CSV files)
        
        :param fname: the file name from which retrieve the waveform
        """
    
        self.scopetube.load(fname)

    def save(self, fname):
        """
        Save the waveform currently in memory (uses CSV files)
        
        :param fname: the file name in which save the waveform
        """
        self.scopetube.save(fname)

if __name__=='__main__':
    try:
        from Tkinter import Tk
    except ImportError:
        from tkinter import Tk

    root=Tk()

    scope=Scope(root, [], 0, 0)
    
    scope.load('../tests/testpoints.dps')
    scope.redraw()
    root.mainloop()
        


