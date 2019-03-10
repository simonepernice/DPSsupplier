import re

from constants import TPOS, VPOS, CPOS, PPOS

class Dpsfile():
    def __init__(self, points=[]):
        self.points=points
        self.revalunit=re.compile(r"([\+\-]*[0-9]*\.[0-9]+)\s*([a-zA-Z]*)")
        
    def getpoints(self):
        return self.points

    def load(self,  fname, addpoint=None):
        with open(fname) as f:
            l=f.readline()
            while l:
#                print l
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
                if len(self.points)>0 and p[TPOS]<=self.points[-1][TPOS]:
                    raise ValueError('Not monotonic time found '+str(p[TPOS])+' at line'+l)
                p=tuple(p)
                if addpoint is not None: 
                    addpoint(p)
                else:
                    self.points.append(p)
                l=f.readline()
                
#        print self.points
        return self.points

    def convert(self, val):
        try:
            return float(val)
        except Exception:
            fields=self.revalunit.match(val)
            if fields:
                values=fields.groups()
                return float(values[0])*{'T':1e12, 'G':1e9, 'M':1e6, 'k':1e3, '':1, 'm':1e-3, 'u':1e-6, 'n':1e-9, 'p':1e-12}[values[1]]
            raise ValueError('Not understood number'+val)
        
    def save(self, fname):
        with open(fname, 'w') as f:
            for p in self.points:
                comma=''
                for v in p:
                    f.write(comma)
                    f.write(str(v))
                    comma=','
                f.write('\n')
