# coding: utf-8

"""
DPS supplier waveform .

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


__author__ = "Simone Pernice"
__copyright__ = "Copyright 2019, DPS supplier"
__credits__ = ["Simone Pernice"]
__license__ = "GNU GPL v3.0"
__version__ = "0.9.0"
__date__ = "16 April 2019"
__maintainer__ = "Simone Pernice"
__email__ = "perniceb@libero.it"
__status__ = "Development"

class Point():
    # Position of values on dps files
    TPOS = 0
    VPOS = 1
    CPOS = 2
    PPOS = 3

    """
    Point represent the value of voltage, current and power in a given time instant.

    """

    def __init__(self, t, v, c, p=None, t0=None):
        self.v = v
        self.c = c
        self.p = v * c if p is None else p
        self.t = t if t0 is None else t - t0        

    @classmethod
    def fromlist(cls, list, t0=0):
        if len(list) > 4:
            return cls(list[0], list[1], list[2], list[3], t0)
        else:
            return cls(list[0], list[1], list[2], t0=t0)
    
    @classmethod    
    def fromstring(cls, string):
        i=0
        p=[]
        for v in string.split(','):
            try:
                p.append(convert(v))
            except Exception:
                print('Not understood value '+v+' at line '+string+' using the previous one')
                p.append(-1.)
            i+=1
        if i<4:#Try to add what is missing
            if i==Point.PPOS:#power missing
               p.append(p[Point.VPOS]*p[Point.CPOS])                        
            else: 
                while i < 4:
                    p.append(-1.)
                    i+=1

        return cls.fromlist(p)

    def getv(self):
        return self.v

    def getc(self):
        return self.c

    def getp(self):
        return self.p
    
    def gett(self):
        return self.t

    def addtime(self, dtime):
        self.t += dtime
        


REVALUNIT=re.compile(r"([\+\-]*[0-9]*\.[0-9]+)\s*([a-zA-Z]*)")
    
def convert(val):
    """
    Convert a value read from file to float. It understands engineer notation. 

    :param val: the value to convert.
    :returns: the floating value converted.

    """      
    try:
        return float(val)
    except Exception:
        fields=REVALUNIT.match(val)
        if fields:
            values=fields.groups()
            return float(values[0])*{'T':1e12, 'G':1e9, 'M':1e6, 'k':1e3, '':1, 'm':1e-3, 'u':1e-6, 'n':1e-9, 'p':1e-12}[values[1]]
        raise ValueError('Not understood number'+val)    

class Waveform():

    """
    DSPfile contains a set of points (time, voltage, current, power) measured or to generate on the DPS.

    """
    def __init__(self):
        """
        Create a DSP file.

        :param points: is the list of points cointained, do not pass to begin with empty list.
        :returns: a new instance of DPS file  

        """
        self.points=[]
    
    def append_dt(self, point):
        if len(self.points) > 0:
            point.addtime(self.points[-1])
        self.points.append(point)

    def append_t(self,  point):
        if len(self.points)>0 and point.gett() <= self.points[-1].gett():
            raise ValueError('Not monotonic time found '+str(point))
        self.points.append(point)

    def findtime(self, t):
        for r in range(len(self.points)):
            if self.points[r].gett() > t :
                break
        else:
            r=len(self.points)
        return r
        
    def insert(self, point):
        self.points.insert(self.findtime(point.gett(), point))
    
    def modify(self, i, point):
        self.points[i] = point
    
    def delete(self, i):
        del self.point[i]


    def __iter__(self):
        self.iterpoint=0
        return self

    def __next__(self): # Python 3
        return next()

    def next(self): # Python 2
        if len(self.points) < selt.iterpoint+1:
            raise StopIteration
        else:
            start = self.iterpoint
            self.iterpoint += 1
            return self.points[start, ] - 1
            
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
            fields=self.REVALUNIT.match(val)
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
