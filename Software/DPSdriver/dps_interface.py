#!/usr/bin/env python
# coding: utf-8

"""
DPS supplier main interface.

This is the main interface through which is possible to interact to the DPS supplier.
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

from scope import Scope
from dps_driver import DPSdriver
from mem_interface import Meminterface
from wve_interface import Wveinterface
from constants import ENTRYWIDTH, VCOL, CCOL, PCOL, TPOS, PROTEXCEED
from dpsfile import Dpsfile
from gridlayoutrowinsert import insertlabelrow, insertentryrow
from poller import Poller
from waver import Waver
from txtinterface import Txtinterface

try:
    from Tkinter import Label, Checkbutton, Entry, Scale, IntVar, StringVar, DoubleVar, E, W, NORMAL, Menu, PhotoImage
    import tkMessageBox
    import tkFileDialog
    from ttk import Separator
except ImportError:
    from tkinter import Label, Checkbutton, Entry, Scale, IntVar, StringVar, DoubleVar, E, W, NORMAL, Menu, PhotoImage
    from tkinter import messagebox as tkMessageBox
    from tkinter import filedialog as tkFileDialog
    from tkinter.ttk import Separator

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

class DPSinterface:

    """
    DSPinterface is a Tk graphical interface to drive a DPS power supplier.

    """
    def __init__(self, root):
        """
        Create a DSP interface instance.

        :param root: is the Tk() interface where the DPS will be drawedstring with the prot name i.e. /dev/ttyUSB0 or COM5 for Windows
        :returns: a new instance of DPS graphical interface

        """

        self.root=root
        root.title("DPS power supplier interface")

        self.dps = None
        self.poller = None
        self.waver = None
        self.strtme = time()
        self.dpsfwave = None
        self.maxoutv=5
        self.maxoutc=5

        menubar = Menu(root)
        
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        scopemenu = Menu(menubar, tearoff=0)
        scopemenu.add_command(label="Load sampled points...", command=self.mnucmdloadsmppts)
        scopemenu.add_command(label="Save sampled points as...", command=self.mnucmdsavesmppts)
        menubar.add_cascade(label="Scope", menu=scopemenu)

        wavemenu = Menu(menubar, tearoff=0)
        wavemenu.add_command(label="New wave", command=self.mnucmdnewwve)
        wavemenu.add_command(label="Load wave...", command=self.mnucmdloadwve)
        wavemenu.add_command(label="Edit wave...", command=self.mnucmdedtwve)
        wavemenu.add_command(label="Save wave as...", command=self.mnucmdsavewve)
        menubar.add_cascade(label="Wave", menu=wavemenu)
 
        memmenu = Menu(menubar, tearoff=0)
        memmenu.add_command(label="Edit memories...", command=self.mnucmdedtmem)
        menubar.add_cascade(label="Memory", menu=memmenu)
  
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help...", command=self.mnucmdhelp)
        helpmenu.add_command(label="About...", command=self.mnucmdabout)
        menubar.add_cascade(label="Help", menu=helpmenu)

        root.config(menu=menubar)

        row = 0
        col = 0
        rowspan = 1
        colspan = 1
        insertlabelrow(root, row, col, ("Serial: ", None, "Addr,Baud: "), E)
        col +=  colspan
        self.svardpsport=StringVar()
        self.svardpsport.set('/dev/ttyUSB0')        
        self.entryserport=Entry(root, textvariable=self.svardpsport, width=ENTRYWIDTH, justify='right')
        self.entryserport.grid(row=row, column=col, sticky=W)                
        col+=colspan
        col+=colspan
        self.svardpsaddbrt=StringVar()
        self.svardpsaddbrt.set('1, 9600')
        self.entrydpsadd=Entry(root, textvariable=self.svardpsaddbrt, width=ENTRYWIDTH, justify='right')
        self.entrydpsadd.grid(row=row, column=col, sticky=W)
        col+=colspan
        colspan=2
        self.ivarconctd=IntVar()
        self.ivarconctd.set(0)
        Checkbutton(root, variable=self.ivarconctd, text='Connect', command=self.butcmdconnect).grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        
        row+=rowspan
        col=0
        colspan=1
        Separator(root, orient='horizontal').grid(row=row, columnspan=8, sticky=E+W, pady=8)

        row+=rowspan
        rowspan=1
        colspan=2
        col=0
        self.ivarbrghtnes=IntVar()
        s=Scale(root, label='Brightness', variable=self.ivarbrghtnes, from_=0, to=5, resolution=1, orient="horizontal")
        s.bind("<ButtonRelease-1>", self.sclbndbrghtnss)
        s.grid(row=row, column=col, columnspan=colspan, sticky=E+W)                
        col+=colspan
        colspan=1
        Label(root, text="Model: ").grid(row=row, column=col, sticky=E)        
        col+=colspan
        self.ivarmodel=IntVar()
        Entry(root, textvariable=self.ivarmodel, state="readonly", width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)        
        col+=colspan
        colspan=2
        self.ivarsetmem=IntVar()
        s=Scale(root, label='Mem Recall', variable=self.ivarsetmem, from_=1, to=9, resolution=1, orient="horizontal")
        s.bind("<ButtonRelease-1>", self.sclbndmemory)
        s.grid(row=row, column=col, columnspan=colspan, sticky=E+W)
  
        row+=rowspan
        colspan=1
        col=0
        insertlabelrow(root, row, col, (("Vinp [V]: ", VCOL), None, "Out Mode: ", None, "Protection: "), E)
        self.dvarvinp=DoubleVar()
        self.svarwrmde=StringVar()
        self.setworkmode(0)
        self.svarprot=StringVar()
        self.setprotection(0)
        insertentryrow(root, row, col, (None, self.dvarvinp, None, self.svarwrmde, None, self.svarprot), 'right', W, 'readonly')

        colspan=1
        row+=rowspan
        col=0
        insertlabelrow(root, row, col, (("Vmax [V]: ", VCOL), None, ("Cmax [A]: ", CCOL), None, ("Pmax [W]: ", PCOL)), E)
        self.dvarvmaxm0=DoubleVar()
        self.dvarcmaxm0=DoubleVar()
        self.dvarpmaxm0=DoubleVar()
        entries=insertentryrow(root, row, col, (None, self.dvarvmaxm0, None, self.dvarcmaxm0, None, self.dvarpmaxm0), 'right', W)
        for e, f in zip(entries, (self.entbndvmax, self.entbndcmax, self.entbndpmax)):
            e.bind('<FocusOut>', f)
            e.bind('<Return>', f)
        
        row+=rowspan
        col=0
        insertlabelrow(root, row, col, (("Vout [V]: ", VCOL), None, ("Cout [A]: ", CCOL), None, ("Pout [W]: ", PCOL)), E)
        self.dvarvout=DoubleVar()
        self.dvarcout=DoubleVar()
        self.dvarpout=DoubleVar()
        insertentryrow(root, row, col, (None, self.dvarvout, None, self.dvarcout, None, self.dvarpout), 'right', W, 'readonly')

        row+=rowspan
        col=0
        self.scope=Scope(root, [], row, col)
        
        row+=9
        col=4
        Label(root, text="Rte[s/Sa]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarsecsmp=DoubleVar()
        self.dvarsecsmp.set(self.scope.sampletime())
        e=Entry(root, textvariable=self.dvarsecsmp, width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W) 
    
        row+=rowspan
        col=0
        colspan=2
        self.ivaracquire=IntVar()
        self.ivaracquire.set(0)        
        Checkbutton(root, variable=self.ivaracquire, text='Run Acquisition', command=self.butcmdacquire).grid(row=row, column=col, columnspan=2, sticky=E+W)               
        col+=colspan
        self.ivarkeylock=IntVar()
        self.ivarkeylock.set(0)
        Checkbutton(root, variable=self.ivarkeylock, text="Key Lock", command=self.butcmdkeylock).grid(row=row, column=col, sticky=E+W, columnspan=colspan)         
        col+=colspan        
        self.ivaroutenab=IntVar()
        self.ivaroutenab.set(0)
        Checkbutton(root, variable=self.ivaroutenab, text="Output Enable", command=self.butcmdoutenable).grid(row=row, column=col, sticky=E+W, columnspan=colspan)    

        row+=rowspan
        col=0
        rowspan=1        
        colspan=3
        self.dvarvscale=DoubleVar()
        self.voltscale=Scale(root, label='Vset [V]', foreground=VCOL, variable=self.dvarvscale, from_=0, to=self.maxoutv, resolution=1, orient="horizontal")#, label='Vset[V]'
        self.voltscale.bind("<ButtonRelease-1>", self.sclbndvolt)
        self.voltscale.grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        col+=colspan
        self.dvarcscale=DoubleVar()
        self.curntscale=Scale(root, label='Cset[A]', foreground=CCOL, variable=self.dvarcscale, from_=0, to=self.maxoutc, resolution=1, orient="horizontal")#,label='Cset[A]'
        self.curntscale.bind("<ButtonRelease-1>", self.sclbndcrnt)
        self.curntscale.grid(row=row, column=col, columnspan=colspan, sticky=E+W)

        row+=rowspan 
        col=0
        self.dvarvscalef=DoubleVar()
        sc=Scale(root, foreground=VCOL, variable=self.dvarvscalef, from_=0, to=0.99, resolution=0.01, orient="horizontal")
        sc.bind("<ButtonRelease-1>", self.sclbndvolt)
        sc.grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        col+=colspan
        self.dvarcscalef=DoubleVar()
        sc=Scale(root, foreground=CCOL, variable=self.dvarcscalef, from_=0, to=0.99, resolution=0.01, orient="horizontal")
        sc.bind("<ButtonRelease-1>", self.sclbndcrnt)
        sc.grid(row=row, column=col, columnspan=colspan, sticky=E+W)

        row+=rowspan
        col=0
        colspan=1
        Separator(root, orient='horizontal').grid(row=row, columnspan=6, sticky=E+W, pady=8)

        row+=rowspan
        colspan=1
        col=0
        Label(root, text="Waveform: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        colspan=3
        self.svarwave=StringVar()
        Entry(root, textvariable=self.svarwave, width=ENTRYWIDTH, justify='right', state='readonly').grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        col+=colspan
        colspan=1
        self.ivarplaywv=IntVar()
        self.ivarplaywv.set(0)        
        Checkbutton(root, variable=self.ivarplaywv, text='Play', command=self.butcmdplaywave).grid(row=row, column=col, sticky=E+W)                        
        col+=colspan
        self.ivarpausewv=IntVar()
        self.ivarpausewv.set(0)        
        Checkbutton(root, variable=self.ivarpausewv, text='Pause', command=self.butcmdpausewave).grid(row=row, column=col, sticky=E+W)
        
        self.scope.update()
        self.scope.redraw()
        
    def sclbndvolt(self, event):
        """
        Voltage scale bind command to set the voltage on the DSP.

        :param event: the event describing what changed

        """    
        if self.isconnected():
            self.dps.set(['vset'],  [self.getvscale()])

    def sclbndcrnt(self, event):
        """
        Current scale bind command to set the current on the DSP.

        :param event: the event describing what changed

        """
        if self.isconnected():
            self.dps.set(['cset'],  [self.getcscale()])
    
    def sclbndmemory(self, event):
        """
        Memory-set bind command to set the memory on the DSP.

        :param event: the event describing what changed

        """
        if self.isconnected():            
            m=self.ivarsetmem.get()
            self.dps.set(['mset'], [m])
            self.updatefields(True)
    
    def sclbndbrghtnss(self, event):
        """
        Brightness bind command to set the brightness on the DSP.

        :param event: the event describing what changed

        """
        if self.isconnected():            
            b=self.ivarbrghtnes.get()
            self.dps.set(['brght'], [b])

    def mnucmdnewwve(self):
        """
        New wave menu command to initialize a new wave.

        """
        self.dpsfwave=Dpsfile()
        self.svarwave.set('unnamed')

    def mnucmdloadwve (self):
        """
        Load wave menu command to load a wave file.

        """    
        fname=tkFileDialog.askopenfilename(initialdir=".", title="Select wave file to load", filetypes=(("dps files","*.dps"), ("all files","*.*")))
        if fname:
            self.svarwave.set(fname)
            self.dpsfwave=Dpsfile()
            self.dpsfwave.load(fname)

    def mnucmdedtwve(self):
        """
        Edit wave menu command to open the edit wave window.

        """
        if self.dpsfwave is not None:
            Wveinterface(self.root, self.dpsfwave.getpoints())
        else:
            tkMessageBox.showinfo('No wave loaded', 'Load or create a new wave file to modify')         

    def mnucmdsavewve(self):
        """
        Save wave menu command to save the current wave in memory.

        """
        if self.dpsfwave is not None:
            fname=tkFileDialog.asksaveasfilename(initialdir=".", title="Select wave file to save", filetypes=(("dps files","*.dps"), ("all files","*.*")))
            if fname:
                self.dpsfwave.save(fname)
                self.svarwave.set(fname)
        else:
            tkMessageBox.showinfo('No wave in memory', 'Load or create a wave file to modify') 

    def mnucmdloadsmppts (self):
        """
        Load sampled points menu command to load in the graphical view sampled before.

        """
        fname=tkFileDialog.askopenfilename(initialdir=".", title="Select data file to load", filetypes=(("dps files","*.dps"), ("all files","*.*")))
        if fname:
            self.scope.load(fname)

    def mnucmdsavesmppts(self):
        """
        Save sampled points menu command to save the last points sampled showed in the graphical view.

        """
        fname=tkFileDialog.asksaveasfilename(initialdir=".", title="Select data file to save", filetypes=(("dps files","*.dps"), ("all files","*.*")))
        if fname:
            self.scope.save(fname)

    def mnucmdedtmem(self):
        """
        Memory menu command to edit the values of preset memories on DSP.

        """
        if self.isconnected():
            Meminterface(self.root, self.dps, self.updatefields)

    def mnucmdabout(self):
        """
        About menu command to show the window with program information.

        """
        Txtinterface(self.root, 'About', 
"""DPS interface is designed by Simone Pernice

This project was born because nothing open source nor for Linux distribution were available.
For question email to me: pernice@libero.com
Version {} relesed on {}
First release on 3rd February 2019 Turin Italy
DPS interface is under licence {}

If you like this program please make a donation with PayPal to simone.pernice@gmail.com""".format(__version__, __date__, __license__))

    def mnucmdhelp(self):
        """
        Help menu command to show basic help on usage.

        """
        Txtinterface(self.root, 'Help', 
"""This is an interface to remote controll a power supplier of DPS series.
To connect to DPS power supplier first link it to the PC through an USB cable.
The data required to connect is on the first row of the graphical interface.
Write the serial address on the first field (COMxx for Windows or 
/dev/ttyUSBx for Linux).
Address and baudrate do not require update because they are the default 
for DPS power supplier. Turn on DPS with up key pressed to change those values.
Press 'Connect' check button and if the device is present it is linked. 
Press again to disconnect.
Once the link is in place all the data on the interface are updated and 
on the DPS the keylock is set. 
The second block of graphical interface contains all data about DPS.
The brightness set which can be changed through the scale regulation.
The model. The memory to recall to preset all parameters.
The input voltage, the output mode cv (constant voltage) or cc (constant current).
The protection mode: none, ovp (over voltage protection), ocp (over current protection), 
opp (over power protection).
The maximum voltage, current and power to provide before triggering the protection.
The current output voltage, current and power.
A time diagram of the DPS output. 
It is possible to play with the mouse on that screen:
- wheel press to fit the highlighted curves
- wheel to zoom in time
- shift+wheel to zoom on Y of the highlighted curves
- ctrl+wheel to change the enabled curves
- left button drag to move the highlighted curve
The same zoom features are available in the fields below the diagram:
- voltage per division, current per division and watt per division
- zero position for voltage, current and power
- check button for voltage, current and power
- time: second per divisions and zero position for time
The sample time is used for the acquisition, the minimum is around 1 second.
The next buttons are:
- Run acquisition: starts a thread that read the DPS status, update the interface 
fields as well as the time diagram
- Key lock: set or reset the DPS key lock. It should be on in order to have faster
communication becase less fields of DPS are read since user can change them only
through the PC interface.
- Output enable to set the DPS on
Eventually there are the voltage and current scale. Thery are split in two:
- the first  is for coarse adjustment accurate at the unit of voltage/current 
- the second is for fine adjustament accurate at the cents of voltage current
On the last block of interface there is a waveform field showing the wave loaded.
Wave is a set of required output voltage and current at give timings. It is possible
play and pause it through the respective commands of the interface.""")

    def butcmdconnect(self):
        """
        Connect check button command to connect to the DSP.

        It reads: serial port address, DPS address and serial speed from other interface fields.
        If it is capable to link to the DPS: 
        - the maximum voltage and current are read and scale maximums set accordingly
        - the DPS current data are read and set accordingly in the interface
        - the localDPS interface is locked so that the user cannot change them but has to go through the graphical interface
         if the DPS is locked the polling is faster because less data needs to be read from DPS 
        - the input fields are disabled
        """
        if self.ivarconctd.get():
            try:
                flds=self.svardpsaddbrt.get().split(',')
                if len(flds)>0:
                    ch=int(flds[0])
                else:
                    ch=1
                if len(flds)>1:
                    br=int(flds[1])
                else:
                    br=9600
                self.dps=DPSdriver(self.svardpsport.get(), ch, br) 
            except Exception as e:
                tkMessageBox.showerror('Error',  'Cannot connect: '+str(e))
                self.ivarconctd.set(0)
                self.dps=None
                return
            
            m=self.dps.get(['model'])
            m=m[0]
            self.ivarmodel.set(m)

            to=m/100
            self.voltscale.config(to=to)
            self.maxoutv=to

            to=m%100
            self.curntscale.config(to=to)
            self.maxoutv=to
            
            self.scope.resetpoints()

            self.ivarkeylock.set(1)
            self.butcmdkeylock()
            self.updatefields(True)
                        
            self.entryserport.config(state='readonly')
            self.entrydpsadd.config(state='readonly')
        else:
            # Stop polling 
            self.ivaracquire.set(0)
            if self.poller:
                self.poller.wake()

            # Stop waveform generation
            self.ivarplaywv.set(0)
            if self.waver:
                self.waver.wake()

            self.dps=None

            self.entryserport.config(state=NORMAL)
            self.entrydpsadd.config(state=NORMAL)

    def butcmdacquire(self):
        """
        Acquire check button command to manage the acquisition thread to read the DSP data.
        If the button is not selected the thread is lunched.
        If the button is selected the thread is stopped.

        """
        if self.ivaracquire.get():
            if not self.isconnected():
                self.ivaracquire.set(0)
                return
            self.scope.resetpoints()
            self.strtme=time()
            self.poller=Poller(self.ivaracquire, self.dvarsecsmp, self.updatefields)            
        else:
            self.poller.wake()

    def butcmdkeylock(self):
        """
        Key lock button command to enable or disable the key lock on DPS remote interface.

        """
        if self.isconnected():
            self.dps.set(['lock'], [self.ivarkeylock.get()])
        else:
            self.ivarkeylock.set(0)

    def butcmdoutenable(self):
        """
        DPS output button command to enable or disable the DPS output power.

        """
        if self.isconnected():
            self.dps.set(['onoff'], [self.ivaroutenab.get()])
        else:
            self.ivaroutenab.set(0)

    def butcmdplaywave(self):
        """
        Wave generator  check button command to manage the wave generation thread to make a waveform on the DSP.
        If the button is not selected the thread is lunched.
        If the button is selected the thread is stopped.

        """    
        if self.ivarplaywv.get():
            if not self.isconnected():
                self.ivarplaywv.set(0)
                return
            if not self.dpsfwave:
                tkMessageBox.showinfo('No wave in memory', 'Load or create a wave file to modify')
                self.ivarplaywv.set(0)
                return
            if not self.ivaroutenab.get():
                self.ivaroutenab.set(1)
                self.butcmdoutenable()
            self.waver=Waver(self.setvcdps, self.ivarplaywv, self.ivarpausewv, self.dpsfwave.getpoints())            
        else:
            self.waver.wake()
        
    def butcmdpausewave(self):
        """
        Wave generator  pause check button command to temporary pause the wave generations.

        """    
        self.waver.wake()

    def entbndvmax(self, event):
        """
        Maximum voltage entry bind to set the protection maximum ouput voltage of the DSP.

        :param event: the event describing what changed

        """
        if self.isconnected():
            if self.dvarvmaxm0.get() > self.maxoutv * PROTEXCEED : self.dvarvmaxm0.set(self.maxoutv * PROTEXCEED)
            elif self.dvarvmaxm0.get() < 0. : self.dvarvmaxm0.set(0.)
            self.dps.set(['m0ovp'], [self.dvarvmaxm0.get()])         

    def entbndcmax(self, event):
        """
        Maximum current entry bind to set the protection maximum output curret of the DSP.

        :param event: the event describing what changed

        """
        if self.isconnected():
            if self.dvarcmaxm0.get() > self.maxoutc * PROTEXCEED : self.dvarcmaxm0.set(self.maxoutc * PROTEXCEED)
            elif self.dvarcmaxm0.get() < 0. : self.dvarcmaxm0.set(0.)            
            self.dps.set(['m0ocp'], [self.dvarcmaxm0.get()])

    def entbndpmax(self, event):
        """
        Maximum power entry bind to set the protection maximum output power of the DSP.

        :param event: the event describing what changed

        """
        if self.isconnected():
            if self.dvarpmaxm0.get() > self.maxoutv * self.maxoutc * PROTEXCEED * PROTEXCEED : self.dvarpmaxm0.set(self.maxoutv * self.maxoutc * PROTEXCEED * PROTEXCEED)
            elif self.dvarpmaxm0.get() < 0. : self.dvarcmaxm0.set(0.)             
            self.dps.set(['m0opp'], [self.dvarpmaxm0.get()])
            
    def setvcdps(self, v, c):
        """
        Set the DPS output voltage and current moving their scales accordingly.

        :param v: the required voltage, if negative it is not changed
        :param c: the required current, if negative it is not changed

        """
        if v>=0:
            if c>=0:
                self.setvscale(v)
                self.setcscale(c)
                self.dps.set(['vset', 'cset'], [v, c])
            else:
                self.setvscale(v)
                self.dps.set(['vset'], [v])
        elif c>=0:
            self.setcscale(c)
            self.dps.set(['cset'], [c])

    def isconnected(self):
        """
        Check if the DPS is connected, if not display a message.

        :returns: True if connected, False if not

        """
        if self.dps is None:
            tkMessageBox.showinfo('Not connected',  'Enstablish a connection before') 
            return False
        return True

    def setvscale(self, v):
        """
        Set the voltage scale, nothing is changed on the DPS.

        :param v: the voltage to set

        """
        if v > self.maxoutv : v = self.maxoutv
        elif v < 0 : v = 0
        self.dvarvscale.set(int(v))
        self.dvarvscalef.set(round(v-int(v), 2))

    def getvscale(self):
        """
        Get the voltage scale set value.

        :returns: the voltage set

        """
        return self.dvarvscale.get()+self.dvarvscalef.get()

    def setcscale(self, c):
        """
        Set the current scale, nothing is changed on the DPS.

        :param c: the current to set

        """    
        if c > self.maxoutc : c = self.maxoutc
        elif c < 0 : c = 0        
        self.dvarcscale.set(int(c))
        self.dvarcscalef.set(round(c-int(c), 2))

    def getcscale(self):
        """
        Get the current scale set value.

        :returns: the current set

        """    
        return self.dvarcscale.get()+self.dvarcscalef.get()
        
    def updatefields(self, forcereadall=False):
        """
        Reads data stored in DPS and updates the interface fields accordingly. 
        
        In order to be as fast as possible, if keylock is enabled, reads only the fields that can change without uses access.
        If keylock is disabled all the fields are read because user may have changed something from the interface.

        :param forcereadall: if True read and update all the DPS fields regardless of the keylock status
        :returns: the point read. A point is made by (time, voltage, current, power)

        """      
        if not forcereadall and self.ivarkeylock.get(): # If user keep locked fewer data are read, otherwise all 
            data=self.dps.get(['vout', 'cout', 'pout', 'vinp', 'lock', 'prot', 'cvcc'])                     
            self.dvarvout.set(data[0])
            self.dvarcout.set(data[1])
            self.dvarpout.set(data[2])
            self.dvarvinp.set(data[3])
            self.ivarkeylock.set(data[4])
            self.setprotection(data[5])
            self.setworkmode(data[6])
            vcp=data[0:3]

        else: # All data is read
            data=self.dps.get(['vset', 'cset',  'vout', 'cout', 'pout', 'vinp', 'lock', 'prot', 'cvcc', 'onoff', 'brght', 'mset', 'm0ovp', 'm0ocp', 'm0opp'])
            self.setvscale(data[0])
            self.setcscale(data[1])
            self.dvarvout.set(data[2])
            self.dvarcout.set(data[3])
            self.dvarpout.set(data[4])
            self.dvarvinp.set(data[5])
            self.ivarkeylock.set(data[6])
            self.setprotection(data[7])
            self.setworkmode(data[8])
            self.ivaroutenab.set(data[9])
            self.ivarbrghtnes.set(data[10])
            self.ivarsetmem.set(data[11])
            self.dvarvmaxm0.set(data[12])
            self.dvarcmaxm0.set(data[13])
            self.dvarpmaxm0.set(data[14])
            vcp=data[2:5]

        vcp.insert(TPOS, time()-self.strtme)
        self.scope.addpoint(vcp)
        return vcp        

    def setprotection(self, p):
        """
        Set the protection field with an user readable string explaining the DPS protection status.

        :param p: the protection statu returned by the DPS

        """
        self.svarprot.set({0: 'none', 1: 'ovp', 2: 'ocp', 3: 'opp'}[p])

    def setworkmode(self, wm):
        """
        Set the workmode field with an user readable string explaining the DPS work mode.

        :param wm: the working mode returned by the DPS

        """
        self.svarwrmde.set({0: 'cv', 1: 'cc'}[wm])

if __name__=='__main__':
    try:
        from Tkinter import Tk
    except ImportError:
        from tkinter import Tk

    root=Tk()

    try:
        root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='pwrsup.png'))
    except:
        print ('It is not possible to load the application icon')

    my_gui=DPSinterface(root)
    root.mainloop()
