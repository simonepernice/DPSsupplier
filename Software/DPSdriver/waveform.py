# coding: utf-8

"""
DPS supplier waveform .

This file contains the classes required to hide DPS waveform interface internal structure 
in classe. It is not used. At the moment the waveform is represnted as a list of:
time (absolute), voltage, current, power. In the end it was not used to avoid
rewriting of several other files.

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

REVALUNIT=re.compile(r"([\+\-]*[0-9]*\.[0-9]+)\s*([a-zA-Z]*)")
   
def convert(val):
    """
    Convert a string value read from file to float. It understands engineer notation. 

    :param val: the string containing the value to convert.
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

class Point():
#    # Position of values on dps list
#    TPOS = 0
#    VPOS = 1
#    CPOS = 2
#    PPOS = 3

    """
    Point represent the value of voltage, current and power in a given absolute time instant.

    """

    def __init__(self, t, v, c, p=None, t0=None):
        """
        Make a new point.
        
        Make a new point knowing its time, voltage, current.

        :param t: the absolute time istant of the pointe. Define t0 to make t relative to t0
        :param v: the voltage at t. Use None to copy later from another point.
        :param c: the current at t. Use None to copy later from another point.
        :param p: the power. Use None to compute from c and v if availables otherwise can can be copied later from another point.
        :param t0: the begin time reference for t
        :returns: the new point

        """        
        self.v = v
        self.c = c
        self.p = v * c if p is None and v is not None and c is not None else p
        self.t = t if t0 is None else t - t0
        if self.t is None or self.t < 0:
            raise ValueError('None or negative time is not allowed for a point')

    @classmethod
    def frompoint(cls, point):
        return cls(point.t, point.v, point.c, point.p)

    @classmethod
    def fromlist(cls, list, t0=None):
        if len(list) > 4:
            return cls(list[Point.TPOS], list[Point.VPOS], list[Point.CPOS], list[Point.PPOS], t0)
        else:
            return cls(list[Point.TPOS], list[Point.VPOS], list[Point.CPOS], t0=t0)
    
    @classmethod    
    def fromstring(cls, string):
        """
        Make a new point from a string.
        
        :param string: contains time, voltage, current and power can be expressed in engineer notation. 
        If something missing is set to None to be copied from previous poin later
        :returns: the new point

        """                
        i=0
        p=[]
        for v in string.split(','):
            try:
                p.append(convert(v))
            except Exception:
                print('Not understood a value on the line '+string+' it will be used the previous one')
                p.append(None)
            i+=1
        if i<4: # Try to add what is missing
            if i==3 and p[2] is not None and p[1] is not None: # Power missing
               p.append(p[2] * p[1])                        
            else: # At list current and power are missing if not more
                while i < 4:
                    p.append(None)
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

    def copymissingfrom(self, prevpoint):
        if prevpoint is None:
            if self.v is None: self.v = 0.
            if self.c is None: self.c = 0.
            if self.p is None: self.p = self.v * self.c
        else:
            if self.v is None: self.v = prevpoint.v
            if self.c is None: self.c = prevpoint.c
            if self.p is None: self.p = prevpoint.p

    def deltatimefrom(self, prevpoint):
        if prevpoint is not None: self.t += prevpoint.t

    def __le__(self, point):
        return self.t <= point.t

    def __str__(self):
        return '{}, {}, {}, {}\n'.format(self.t,  self.v,  self.c, self.p)

    def copywhatless(self, otherpoint):
        if otherpoint.t < self.t: self.t = otherpoint.t
        if otherpoint.v < self.v: self.v = otherpoint.v
        if otherpoint.c < self.t: self.c = otherpoint.c
        if otherpoint.p < self.p: self.p = otherpoint.p

    def copywhatmore(self, otherpoint):
        if otherpoint.t > self.t: self.t = otherpoint.t
        if otherpoint.v > self.v: self.v = otherpoint.v
        if otherpoint.c > self.t: self.c = otherpoint.c
        if otherpoint.p > self.p: self.p = otherpoint.p


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
        point.copymissingfrom(self.points[-1] if len(self.points) > 0 else None)
        point.deltatimefrom(self.points[-1] if len(self.points) > 0 else None)
        self.points.append(point)

    def append_t(self,  point):
        point.copymissingfrom(self.points[-1] if len(self.points) > 0 else None)
        if len(self.points)>0 and point <= self.points[-1]:
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

    def deleteall(self):
        del self.points[:]

    def __iter__(self):
        self.iterpoint=0
        return self

    def __next__(self): # Python 3
        return next()

    def next(self): # Python 2
        beg = self.iterpoint
        end = self.iterpoint+1
        if end >= len(self.points):
            raise StopIteration
        else:
            self.iterpoint += 1
            return self.points[beg:end]
#            
#    def getpoints(self):
#        """
#        Provide the list of points.
#
#        :returns: the list of points of the DPS file  
#
#        """    
#        return self.points

    def load(self,  fname):
        """
        Load a DSPfile from a file.

        :param fname: the file name where the dps file is content. The list is saved as csv (comma separated values).
        :returns: the list of points content on the DPS file  

        """    
        with open(fname) as f:
            line = f.readline()
            while line:
                self.append_t(Point.fromstring(line))
                line = f.readline()
        
    def save(self, fname):
        """
        Save DSPfile to a file.

        :param fname: the file name where the dps file is saved. The list is saved as csv (comma separated values).

        """    
        with open(fname, 'w') as f:
            for point in self.points:
                f.write(str(point))

    def lasttwopoints(self):
        if len(self.points) > 1:
            return self.points[-2:]
        return None

    def getminmax(self, enablist):
        if len(self.points) < 1: return None
        pmin = Point.frompoint(self.points[0])
        pmax = Point.frompoint(self.points[0])
        for p in self.points[1:]:
            pmin.copywhatless(p)
            pmax.copywhatmore(p)
        return (pmin, pmax)
