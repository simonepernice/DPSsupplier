# coding: utf-8

"""
Class used to show help text.

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

from toplevel import maketoplevel

try:
    from Tkinter import Text, END, DISABLED, Button, BOTH
except ImportError:
    from tkinter import Text, END, DISABLED, Button, BOTH

__author__ = "Simone Pernice"
__copyright__ = "Copyright 2019, DPS supplier"
__credits__ = ["Simone Pernice"]
__license__ = "GNU GPL v3.0"
__version__ = "0.9.0"
__date__ = "16 April 2019"
__maintainer__ = "Simone Pernice"
__email__ = "perniceb@libero.it"
__status__ = "Development"

class Txtinterface:
    """
    Txtinterface create a new windows (modal) with text the user want to display.
    
    It is possible to set width or height, if not porvided thery are computed to fit the text.
    It can read the content from a file or the help string can be provided.
    """

    def __init__(self, prevroot,  title,  txt,  readfromfile=False, width=-1, height=-1):
        """
        Build a new text interface.
        
        :param prevroot: is the higher rate window
        :param title: is the new window title
        :param txt: is the text to show or the file name to read the text from
        :param readfromfile: (optional, default false) if true try to read the content from a file 
        :param width: the number of characters for width, if not set it is automatically computed
        :param height: the number fo characters for height, if not set it is automatically computed
        :returns: a new class
        """

        self.root=maketoplevel(prevroot, True)
        self.root.title(title)
        
        if width<0 or height<0:
            h=0
            w=0
            for line in txt.split('\n'):
                if len(line) > w: w = len(line)
                h+=1
            if width < 0: width = w
            if height < 0: height = h

        outputtext=Text(self.root, width=width, height=height)
        
        if readfromfile:
            with open(txt) as infile:
                outputtext.insert(END, infile.read())
        else:
             outputtext.insert(END, txt)
        outputtext.config(state=DISABLED)
        
        outputtext.pack(fill=BOTH, expand=1)
        
        Button(self.root, text="OK", command=self.butcmdok).pack()   
    
    def butcmdok(self):
        """
        Close the windws if the OK butto is pressed.
        """
        self.root.destroy()

if __name__=='__main__':
    try:
        from Tkinter import Tk
    except ImportError:
        from tkinter import Tk

    root=Tk()
    my_gui=Txtinterface(root,  'info',  'This is just\Several lines of \ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext')
    root.mainloop()
