# coding: utf-8

"""
This file contains the constats used over the program.

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

__author__ = "Simone Pernice"
__copyright__ = "Copyright 2019, DPS supplier"
__credits__ = ["Simone Pernice"]
__license__ = "GNU GPL v3.0"
__version__ = "0.9.0"
__date__ = "16 April 2019"
__maintainer__ = "Simone Pernice"
__email__ = "perniceb@libero.it"
__status__ = "Development"

# Entry characters width used for all iuput fields
ENTRYWIDTH=10

# Display oscillocoope graphic curves use the following settings
XDIV = 10.
YDIV = 10.
GRIDDASH = (1, 6)
GRIDCOL = 'gray80'
VCOL = 'green3'
CCOL = 'yellow3'
PCOL = 'magenta3'
BCOL = 'black'
MINSAMPLETIME = 1.

# Wave editor table size
TABLEROW = 8
TABLECOL = 4
CLIPROW = 6

# Position of values on dps files
TPOS = 0
VPOS = 1
CPOS = 2
PPOS = 3

# Coefficient setting how mach the protection can exceed the maximum setting value
PROTEXCEED = 1.1
