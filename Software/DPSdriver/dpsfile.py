# coding: utf-8

"""
DPS supplier file manager.

This is the class with contains file of time, voltage, current and power.
The file can be sampled by the dps interface or made from the wave interface.
It is also possible to edit that file by hand, in that case more facility are availble:
- do not write a parameter if it is equals to the one before
- power is autocomputed from voltage and current
- engineer notation is available 
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

import re

from constants import TPOS, VPOS, CPOS, PPOS

__author__ = "Simone Pernice"
__copyright__ = "Copyright 2019, DPS supplier"
__credits__ = ["Simone Pernice"]
__license__ = "GNU GPL v3.0"
__version__ = "0.9.0"
__date__ = "16 April 2019"
__maintainer__ = "Simone Pernice"
__email__ = "perniceb@libero.it"
__status__ = "Development"

class Dpsfile():

    """
    DSPfile contains a set of points (time, voltage, current, power) measured or to generate on the DPS.

    """
    def __init__(self, points=[]):
        """
        Create a DSP file.

        :param points: is the list of points cointained, do not pass to begin with empty list.
        :returns: a new instance of DPS file  

        """
        self.points=points
        self.revalunit=re.compile(r"([\+\-]*[0-9]*\.[0-9]+)\s*([a-zA-Z]*)")
        
    def getpoints(self):
        """
        Provide the list of points.

        :returns: the list of points of the DPS file  

        """    
        return self.points

    def load(self,  fname):
        """
        Load a DSPfile from a file.

        :param fname: the file name where the dps file is content. The list is saved as csv (comma separated values).
        :returns: the list of points content on the DPS file  

        """    
        with open(fname) as f:
            l=f.readline()
            while l:
                i=0
                p=[]
                for v in l.split(','):
                    try:
                        p.append(self.convert(v))
                    except Exception:
                        print('Not understood value '+v+' at line '+l+' using the previous one')
                        if len(self.points)>0:
                            p.append(self.points[-1][i])
                        else:
                            p.append(0.)
                    i+=1
                while i<4:#Try to add what is missing
                    if i==PPOS:#power missing
                       p.append(p[VPOS]*p[CPOS])                        
                    elif len(self.points)>0:#voltage or current missing copy from previous row
                        p.append(self.points[-1][i])
                    else:#on the first row add 0.
                        p.append(0.)
                    i+=1
                if len(self.points)>0 and p[TPOS]<=self.points[-1][TPOS]:
                    raise ValueError('Not monotonic time found '+str(p[TPOS])+' at line'+l)
                p=tuple(p)

                self.points.append(p)
                l=f.readline()
                
        return self.points

    def convert(self, val):
        """
        Convert a value read from file to float. It understands engineer notation. 

        :param val: the value to convert.
        :returns: the floating value converted.

        """      
        try:
            return float(val)
        except Exception:
            fields=self.revalunit.match(val)
            if fields:
                values=fields.groups()
                return float(values[0])*{'T':1e12, 'G':1e9, 'M':1e6, 'k':1e3, '':1, 'm':1e-3, 'u':1e-6, 'n':1e-9, 'p':1e-12}[values[1]]
            raise ValueError('Not understood number'+val)
        
    def save(self, fname):
        """
        Save DSPfile to a file.

        :param fname: the file name where the dps file is saved. The list is saved as csv (comma separated values).

        """    
        with open(fname, 'w') as f:
            for p in self.points:
                comma=''
                for v in p:
                    f.write(comma)
                    f.write(str(v))
                    comma=','
                f.write('\n')
