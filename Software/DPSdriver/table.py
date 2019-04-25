# coding: utf-8

"""
DPS supplier table .

This file contains the classes required build a table used to view a waveform points

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

from constants import ENTRYWIDTH, TPOS
from gridlayoutrowinsert import insertlabelrow

try:
    from Tkinter import Label, DoubleVar, IntVar, Button, E, W, Entry
except ImportError:
    from tkinter import Label, DoubleVar, IntVar, Button, E, W, Entry

__author__ = "Simone Pernice"
__copyright__ = "Copyright 2019, DPS supplier"
__credits__ = ["Simone Pernice"]
__license__ = "GNU GPL v3.0"
__version__ = "0.9.0"
__date__ = "16 April 2019"
__maintainer__ = "Simone Pernice"
__email__ = "perniceb@libero.it"
__status__ = "Development"

class Table:
    """
    Table create the instance of a table on a grid layout: it is made by labels plus button to move among lines. 
    
    The table show a list provided as data plus a step number on the most left column.
    The table is based on a first row of static lables containing the column names.
    Buttons to go:
    - 1 line up or down
    - 1 page up or down
    - top or bottom
    - go to a given time or step
    """
    
    def __init__(self, root,  data,  labels, row0,  col0, NROWS, NCOLS):
        """
        Build a class a table showing a table with waveform on grid layout.

        :param root: the main window.
        :param data: the data to show.
        :param labels: the table labels.
        :param row0: the table beginning row.
        :param col0: the table beginning column.
        :param NROWS: the table number of rows: if there are few rows not all the move buttons are displayed.
        :param NCOLS: the table number of columns of data to display.
        :returns: the table instance.
        """
        self.root=root
        self.data=data
        self.NROWS=NROWS
        self.firstvisiblerow=0

        insertlabelrow(root, row0, col0, labels)
        
        self.dvararoutput=[]
        for r in range(NROWS):
            line=[]
            for c in range(NCOLS):
                s=DoubleVar()
                line.append(s)
                Label(root, textvariable=s, width=ENTRYWIDTH, relief='ridge', justify='right').grid(row=row0+r+1, column=col0+c)
            self.dvararoutput.append(line)
        
        colspan=1
        rowspan=1
        row=row0+1
        col=col0+NCOLS        
        if NROWS>=2:
            Button(root, text="Line up", command=self.butcmdlneup).grid(row=row, column=col, sticky=E+W, padx=8)
            row+=rowspan
            if NROWS>=4:
                Button(root, text="Page up", command=self.butcmdpgeup).grid(row=row, column=col, sticky=E+W, padx=8)
                row+=rowspan
                if NROWS>=6:
                    Button(root, text="Top", command=self.butcmdtop).grid(row=row, column=col, sticky=E+W, padx=8)        
                    row+=rowspan
                    if NROWS>=8:
                        Button(root, text="Goto Time", command=self.butcmdgototime).grid(row=row, column=col, sticky=E+W, padx=8)        
                        col+=colspan
                        self.dvargototime=DoubleVar()
                        Entry(root, textvariable=self.dvargototime, width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)
                        row=NROWS-3
                        col=col0+NCOLS
                        Button(root, text="Goto Step", command=self.butcmdgotostep).grid(row=row, column=col, sticky=E+W, padx=8)        
                        col+=colspan
                        self.ivargotostep=IntVar()
                        Entry(root, textvariable=self.ivargotostep, width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)
                        row+=rowspan
                    col=col0+NCOLS
                    Button(root, text="Bottom", command=self.butcmdbottom).grid(row=row, column=col, sticky=E+W, padx=8)
                    row+=rowspan
                Button(root, text="Page down", command=self.butcmdpgedwn).grid(row=row, column=col, sticky=E+W, padx=8)
                row+=rowspan
            Button(root, text="Line down", command=self.butcmdlnedwn).grid(row=row, column=col, sticky=E+W, padx=8)      
        
        self.updateview()
    
    def getfistvisiblerow(self):
        """
        To get the pointer to the first row.
        
        :returns: the index of the first row showed.
        """
        return self.firstvisiblerow

    def updateview(self):
        """
        Updates the data displayed on the table.
        """
        if self.firstvisiblerow<0:
            self.firstvisiblerow=0
        elif self.firstvisiblerow>=len(self.data):
            self.firstvisiblerow=len(self.data)-1        
    
        row=self.firstvisiblerow
        rows=0
        for orow, drow in zip(self.dvararoutput, self.data[row:row+self.NROWS]):
            orow[0].set(row)
            row+=1
            rows+=1
            for ocol, dcol in zip(orow[1:], drow):
                ocol.set(round(dcol, 2))

        while rows<self.NROWS:#clean next fields not written if eny
            for ocol in self.dvararoutput[rows]:
                ocol.set('')
            rows+=1

    def butcmdgototime(self):
        """
        Go to the time set in the time field.
        """
        self.firstvisiblerow=self.findtime(self.dvargototime.get())-1
        self.updateview()

    def butcmdgotostep(self):
        """
        Go to the step set in the step field.
        """        
        self.firstvisiblerow=self.ivargotostep.get()
        self.updateview()

    def butcmdlneup(self):
        """
        Go up by one line.
        """        
        self.firstvisiblerow-=1
        self.updateview()

    def butcmdpgeup(self):
        """
        Go up by one page.
        """
        self.firstvisiblerow-=(self.NROWS-1)
        self.updateview()

    def butcmdtop(self):
        """
        Go to the first line.
        """
        self.firstvisiblerow=0
        self.updateview()

    def butcmdlnedwn(self):
        """
        Go down by one line.
        """
        self.firstvisiblerow+=1
        self.updateview()

    def butcmdpgedwn(self):
        """
        Go down by one page.
        """
        self.firstvisiblerow+=(self.NROWS-1)
        self.updateview()

    def butcmdbottom(self):
        """
        Go to the last line.
        """
        self.firstvisiblerow=len(self.data)-1
        self.updateview()
    
    def findtime(self, t):
        """
        Find the sample with time just after t.
        
        :param t: the time to serach for
        :returns: the index of the list with time just after t
        """
        for r in range(len(self.data)):
            if self.data[r][TPOS]>t :
                break
        else:
            r=len(self.data)
        return r

if __name__=='__main__':
    try:
        from Tkinter import Tk
    except ImportError:
        from tkinter import Tk

    root=Tk()
    data=[]
    table=Table(root, data,  (('step', 'black'), ('time [s]', 'black'), ('voltage [V]', 'red'), ('current [A]', 'blue')), 0, 0, 10, 4)
    for r in range(20):
        l=[]
        for c in range(1, 5):
            l.append(r*10+c)
        data.append(l)

    table.updateview()
    root.mainloop()
