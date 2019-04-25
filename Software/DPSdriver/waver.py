# coding: utf-8

"""
Waveve reproduces a wave designed by user ad DPS output.

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

from threading import Thread, Event
from time import time

from constants import TPOS, CPOS, VPOS

__author__ = "Simone Pernice"
__copyright__ = "Copyright 2019, DPS supplier"
__credits__ = ["Simone Pernice"]
__license__ = "GNU GPL v3.0"
__version__ = "0.9.0"
__date__ = "16 April 2019"
__maintainer__ = "Simone Pernice"
__email__ = "perniceb@libero.it"
__status__ = "Development"

class Waver (Thread):
    """
    Waver is a Thread to play a wave prevously write by the user
    """

    def __init__(self, setvcdps, ivarwvplay, ivarwvpause, wave):
        """
        Make Waver thread instance and start it
        
        :param setvcdps: is the function to call when a new voltage or current is set on DPS
        :param ivarwvplay: is an IntVariable with play status (1: play, 0: stop). When 0 the thread die
        :param ivarwvpause: is an IntVariable with pause status (1: pause, 0: play). When 0 the thread die
        :param wave: is the list of data to play
        """
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
        """
        Recall the function to set voltage and current on DPS.
        
        Only what is changed (voltage, current or both) is update to make the call faster.
        
        :param v: the new voltage
        :param c: the new current
        """
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
        """
        Get the elapsed time since the thread started.
        
        :returns: elapsed time since instance was made
        """
        return time()-self.t0
        
    def wake(self):
        """
        The user should wake the thread instance when something is changed (play or pause values).
        
        Otherwise it has to wait the next writing to make those play/pause settings active.
        """
        self.event.set()

    def checkpause(self):
        """
        Check if the pause is enabled and update the starting time accordingly.
        """
        if self.ivarwvpause.get():
            t1=time()
            self.event.wait()
            self.event.clear()
            self.t0+=time()-t1
            self.checkpause()#verify pause was released
    
    def run(self):
        """
        Run the thread updating the DPS voltage and current.
        
        Checks also play and pause status to behave accordingly"""
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
