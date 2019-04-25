# coding: utf-8

"""
Functions to create Tkinterface windows.

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

import os

try:
    from Tkinter import Toplevel, PhotoImage, Tk
except ImportError:
    from tkinter import Toplevel, PhotoImage, Tk

__author__ = "Simone Pernice"
__copyright__ = "Copyright 2019, DPS supplier"
__credits__ = ["Simone Pernice"]
__license__ = "GNU GPL v3.0"
__version__ = "0.9.0"
__date__ = "16 April 2019"
__maintainer__ = "Simone Pernice"
__email__ = "perniceb@libero.it"
__status__ = "Development"

def maketoplevel(root, modal=False):
    """
    Make a toplevel window children of root.
    
    :param root: the main window
    :param modal: if the chield window as to be modal
    :returns: the child window
    """
    tl=Toplevel(root)
    try:
        root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pwrsup.png')))
    except:
        print ('It is not possible to load the application icon')

    if modal:
        tl.grab_set()
        tl.focus_force()
        
    return tl
    
def makeroot():
    """
    Make the root window of Tkinterface.

    :returns: the root window
    """
    root=Tk()
    try:
        root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pwrsup.png')))
    except:
        print ('It is not possible to load the application icon')
        
    return root
