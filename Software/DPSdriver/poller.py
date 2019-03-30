from threading import Thread, Event
from time import time

class Poller (Thread):

    def __init__(self, ivarpolstate, dvarpoltime, acquiredpoint):
        Thread.__init__(self)

        self.ivarpolstate=ivarpolstate
        self.dvarpoltime=dvarpoltime
        self.acquiredpoint=acquiredpoint
        
        self.event=Event()

        self.start()

    def wake(self):
        self.event.set()
    
    def run(self):
        while self.ivarpolstate.get():
            t=time()
            self.acquiredpoint() 
            t+=self.dvarpoltime.get()-time()
            if t>0:#If t<=0 takes more time to read than acquire so it is working at best effort
                if self.event.wait(t):
                    return
