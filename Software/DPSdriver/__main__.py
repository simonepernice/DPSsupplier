#! /usr/bin/eng python

"""
 DPS interface: an interface for DPS supplier.

(C)2019 - Simone Pernice - pernice@libero.it
This is distributed under GNU LGPL license, see license.txt

"""

from dps_interface import DPSinterface
from toplevel import makeroot

if __name__ == '__main__':
    root = makeroot()

    root.title("DPS supplier driver")

    my_gui = DPSinterface(root)

    root.mainloop()
