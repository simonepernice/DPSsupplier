# coding: utf-8

"""
DPS supplier data poller

This thread is used to poll DPS status and updated the main interface.
It updates also the oscilloscope window with read output voltages.

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

__author__ = "Simone Pernice"
__copyright__ = "Copyright 2019, DPS supplier"
__credits__ = ["Simone Pernice"]
__license__ = "GNU GPL v3.0"
__version__ = "0.9.0"
__date__ = "16 April 2019"
__maintainer__ = "Simone Pernice"
__email__ = "perniceb@libero.it"
__status__ = "Development"

class Poller (Thread):

    """
    Poller is thread to read basic DPS status parameter.

    """
    def __init__(self, ivarpolstate, dvarpoltime, acquiredpoint):
        """
        Create a DPS data poller and start it.

        :param ivarpolstate: is integer variable containing the polling status (1 pollint, 0 no-poll) 
        :param dvarpoltime: is float variable containing the polling time interval 
        :param acquiredpoint: is the function called when a new point is acquired

        """
        Thread.__init__(self)

        self.ivarpolstate=ivarpolstate
        self.dvarpoltime=dvarpoltime
        self.acquiredpoint=acquiredpoint
        
        self.event=Event()

        self.start()

    def wake(self):
        """
        Wake the poller before the next polling.
        
        It checks the polling status to understand if it has to close
        """
        self.event.set()
    
    def run(self):
        """
        Thread running code: acquire a point from DPS and then wait for the required sampling time.
        
        It stops when the acquire button is not selected. The user has to use wake method to interrupt
        the polling soon after polling button is disabled, otherwise the thread will stop at the
        next poll.
        """
        while self.ivarpolstate.get():
            t=time()
            self.acquiredpoint() 
            t+=self.dvarpoltime.get()-time()
            if t>0:#If t<=0 takes more time to read than acquire so it is working at best effort
                if self.event.wait(t):
                    return
