# coding: utf-8

"""
DPS supplier grid label and enty adder.

A couple of functions to insert a row of labels or entries on grid layout.

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

from constants import ENTRYWIDTH, BCOL

__author__ = "Simone Pernice"
__copyright__ = "Copyright 2019, DPS supplier"
__credits__ = ["Simone Pernice"]
__license__ = "GNU GPL v3.0"
__version__ = "0.9.0"
__date__ = "16 April 2019"
__maintainer__ = "Simone Pernice"
__email__ = "perniceb@libero.it"
__status__ = "Development"

try:
    from Tkinter import Label, Entry, NORMAL
except ImportError:
    from tkinter import Label, Entry, NORMAL

def insertlabelrow(root, row, col, names, sticky=''):
    """
    Add a sequence of labels in a row

    :param root: is the window where the labels will be added
    :param row: is the row where the labels will be added 
    :param col: is the beginning column where the labels will be added
    :param names: is the list of strings to use as lablel text, they can be
    a simple string, None to skip, a tuple (string, color) to set the color
    :param sticky: is the stickiness of the labels
    :returns: the list of labels created  

    """
    labellist=[]
    for n in names:
        if n is not None:
            if isinstance(n, tuple):
                t=n[0]
                c=n[1]
            else:
                t=n
                c=BCOL
            l=Label(root, text=t, foreground=c)
            l.grid(row=row, column=col, sticky=sticky)
            labellist.append(l)
        col+=1
    return labellist

def insertentryrow(root, row, col, vars, justify='right', sticky='', state=NORMAL):
    """
    Add a sequence of entries in a row

    :param root: is the window where the entries will be added
    :param row: is the row where the entries will be added 
    :param col: is the beginning column where the entries will be added    
    :param vars: is the IntegerVar, StringVar, FloatVar to associate to the entry,
    use None to skip the entry
    :param justify: is the entry input text justification 
    :param sticky: is the stickiness of the entries
    :param state: is the state of the entries (normal, readonly, ...)
    :returns: the list of entires created  

    """
    entrylist=[]
    r=row
    for v in vars:
        if v is not None:                
            e=Entry(root, textvariable=v, width=ENTRYWIDTH, justify=justify, state=state)
            e.grid(row=r, column=col, sticky=sticky)
            entrylist.append(e)
        col+=1
    return entrylist
