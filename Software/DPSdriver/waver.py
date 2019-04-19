from threading import Thread, Event
from time import time

from constants import TPOS, CPOS, VPOS

class Waver (Thread):

    def __init__(self, setvcdps, ivarwvplay, ivarwvpause, wave):
        Thread.__init__(self)

        self.setvcdps=setvcdps
        self.ivarwvplay=ivarwvplay
        self.ivarwvpause=ivarwvpause
        
        self.wave=wave
        
        self.setvcdps=setvcdps
        
        self.event=Event()

        if abs(self.wave[0][TPOS]-0.)<0.01:
            self.pv=self.wave[0][VPOS]
            self.pc=self.wave[0][CPOS]
            self.index=1
        else:
            self.pv=0
            self.pc=0
            self.index=0
            
        self.setvcdps(self.pv, self.pc)
    
        self.t0=time()

        self.start()

    def setvc(self, v, c):
        if v!=self.pv:
            if c!=self.pc:
                self.setvcdps(v, c)
            else:
                self.setvcdps(v, -1)
        elif c!=self.pc:
            self.setvcdps.set(-1, c)

        self.pv=v
        self.pc=c

    def gettime(self):
        return time()-self.t0
        
    def wake(self):
        self.event.set()

    def checkpause(self):
        if self.ivarwvpause.get():
            t1=time()
            self.event.wait()
            self.event.clear()
            self.t0+=time()-t1
            self.checkpause()#verify pause was released
    
    def run(self):
        while self.ivarwvplay.get():
            self.checkpause()

            ct=self.gettime()
            while self.index<len(self.wave):
                nt=self.wave[self.index][TPOS]
                if nt>ct:
                    break
                self.index+=1
            else:
                self.ivarwvplay.set(0)
                return
            
            if self.event.wait(nt-ct):
                self.event.clear()
            else:
                self.setvc(self.wave[self.index][VPOS], self.wave[self.index][CPOS])
