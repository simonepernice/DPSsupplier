from Tkinter import Label, Checkbutton, Entry, Scale, IntVar, StringVar, DoubleVar, E, W, NORMAL, Menu, PhotoImage
import tkMessageBox
import tkFileDialog

from ttk import Separator
from time import time

from scope import Scope

from dps_driver import DPSdriver
from mem_interface import Meminterface
from wve_interface import Wveinterface
from constants import ENTRYWIDTH, VCOL, CCOL, PCOL, TPOS
from dpsfile import Dpsfile
from gridlayoutrowinsert import insertlabelrow, insertentryrow
from poller import Poller
from waver import Waver
from txtinterface import Txtinterface

class DPSinterface:        
    def __init__(self, root):        
        self.root=root
        root.title("DPS power supplier interface")
        
        self.dps=None
        self.poller=None
        self.waver=None
        self.strtme=time()
        self.dpsfwave=None
        
        menubar=Menu(root)
        
        filemenu=Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        scopemenu=Menu(menubar, tearoff=0)
        scopemenu .add_command(label="Load sampled points...", command=self.mnucmdloadsmppts)
        scopemenu .add_command(label="Save sampled points as...", command=self.mnucmdsavesmppts)
        menubar.add_cascade(label="Scope", menu=scopemenu)
        
        wavemenu=Menu(menubar, tearoff=0)
        wavemenu.add_command(label="New wave", command=self.mnucmdnewwve)
        wavemenu.add_command(label="Load wave...", command=self.mnucmdloadwve)
        wavemenu.add_command(label="Edit wave...", command=self.mnucmdedtwve)
        wavemenu.add_command(label="Save wave as...", command=self.mnucmdsavewve)
        menubar.add_cascade(label="Wave", menu=wavemenu)
 
        memmenu=Menu(menubar, tearoff=0)
        memmenu .add_command(label="Edit memories...", command=self.mnucmdedtmem)
        menubar.add_cascade(label="Memory", menu=memmenu)
  
        helpmenu=Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help...", command=self.mnucmdhelp)
        helpmenu.add_command(label="About...", command=self.mnucmdabout)
        menubar.add_cascade(label="Help", menu=helpmenu)

        root.config(menu=menubar)

        row=0
        col=0
        rowspan=1
        colspan=1
        insertlabelrow(root, row, col, ("Serial: ", None, "Addr,Baud: "), E)
        col+=colspan
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
        self.voltscale=Scale(root, label='Vset [V]', foreground=VCOL, variable=self.dvarvscale, from_=0, to=15, resolution=1, orient="horizontal")#, label='Vset[V]'
        self.voltscale.bind("<ButtonRelease-1>", self.sclbndvolt)
        self.voltscale.grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        col+=colspan
        self.dvarcscale=DoubleVar()
        self.curntscale=Scale(root, label='Cset[A]', foreground=CCOL, variable=self.dvarcscale, from_=0, to=5, resolution=1, orient="horizontal")#,label='Cset[A]'
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
        
    def sclbndvolt(self, event):
        if self.isconnected():
            self.dps.set(['vset'],  [self.getvscale()])

    def sclbndcrnt(self, event):
        if self.isconnected():
            self.dps.set(['cset'],  [self.getcscale()])
    
    def sclbndmemory(self, event):
        if self.isconnected():            
            m=self.ivarsetmem.get()
            self.dps.set(['mset'], [m])
            self.updatefields(True)
    
    def sclbndbrghtnss(self, event):
        if self.isconnected():            
            b=self.ivarbrghtnes.get()
            self.dps.set(['brght'], [b])

    def mnucmdnewwve(self):
        self.dpsfwave=Dpsfile()
        self.svarwave.set('unnamed wave')

    def mnucmdloadwve (self):
        fname=tkFileDialog.askopenfilename(initialdir=".", title="Select wave file to load", filetypes=(("dps files","*.dps"), ("all files","*.*")))
        if fname:
            self.svarwave.set(fname)
            self.dpsfwave=Dpsfile()
            self.dpsfwave.load(fname)

    def mnucmdedtwve(self):
        if self.dpsfwave is not None:
            Wveinterface(self.root, self.dpsfwave.getpoints())
        else:
            tkMessageBox.showinfo('No wave loaded', 'Load or create a new wave file to modify')         

    def mnucmdsavewve(self):
        if self.dpsfwave is not None:
            fname=tkFileDialog.asksaveasfilename(initialdir=".", title="Select wave file to save", filetypes=(("dps files","*.dps"), ("all files","*.*")))
            if fname:
                self.dpsfwave.save(fname)
                self.svarwave.set(fname)
        else:
            tkMessageBox.showinfo('No wave in memory', 'Load or create a wave file to modify') 

    def mnucmdloadsmppts (self):
        fname=tkFileDialog.askopenfilename(initialdir=".", title="Select data file to load", filetypes=(("dps files","*.dps"), ("all files","*.*")))
        if fname:
            self.scope.load(fname)

    def mnucmdsavesmppts(self):
        fname=tkFileDialog.asksaveasfilename(initialdir=".", title="Select data file to save", filetypes=(("dps files","*.dps"), ("all files","*.*")))
        if fname:
            self.scope.save(fname)

    def mnucmdedtmem(self):
        if self.isconnected():
            Meminterface(self.root, self.dps, self.updatefields)

    def mnucmdabout(self):
        Txtinterface(self.root, 'About', 
"""DPS interface is designed by Simone Pernice
For question email to me: pernice@libero.com
Version 1.0 released on 31st March 2019 Turin Italy
DPS interface is under licence GPL 3.0

If you like this program please make a donation with PayPal to simone.pernice@gmail.com""",  width=80,  height=10)

    def mnucmdhelp(self):
        Txtinterface(self.root, 'Help', 
"""This is an interface to remote controll a supplier of DPS series.
This project was born because nothing open source nor for Linux distribution were available.""",  width=80,  height=10)

    def butcmdconnect(self):
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
            self.voltscale.config(to=m/100)
            self.curntscale.config(to=m%100)
            
            self.scope.resetpoints()

            self.ivarkeylock.set(1)
            self.butcmdkeylock()
            self.updatefields(True)
                        
            self.entryserport.config(state='readonly')
            self.entrydpsadd.config(state='readonly')
        else:
            #stop polling 
            self.ivaracquire.set(0)
            if self.poller:
                self.poller.wake()
            #stop waveform generation
            self.ivarplaywv.set(0)
            if self.waver:
                self.waver.wake()
            self.dps=None
            self.entryserport.config(state=NORMAL)
            self.entrydpsadd.config(state=NORMAL)

    def butcmdacquire(self):
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
        if self.isconnected():
            self.dps.set(['lock'], [self.ivarkeylock.get()])
        else:
            self.ivarkeylock.set(0)

    def butcmdoutenable(self):
        if self.isconnected():
            self.dps.set(['onoff'], [self.ivaroutenab.get()])
        else:
            self.ivaroutenab.set(0)

    def butcmdplaywave(self):
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
        self.waver.wake()

#    def toimplement(self):
#        pass
        
    def entbndvmax(self, event):
        if self.isconnected():
            self.dps.set(['m0ovp'], [self.dvarvmaxm0.get()])         

    def entbndcmax(self, event):
        if self.isconnected():
            self.dps.set(['m0ocp'], [self.dvarcmaxm0.get()])

    def entbndpmax(self, event):
        if self.isconnected():
            self.dps.set(['m0opp'], [self.dvarpmaxm0.get()])
            
    def setvcdps(self, v, c):
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
        if self.dps is None:
            tkMessageBox.showinfo('Not connected',  'Enstablish a connection before') 
            return False
        return True

    def setvscale(self, v):
        self.dvarvscale.set(int(v))
        self.dvarvscalef.set(round(v-int(v), 2))

    def getvscale(self):
        return self.dvarvscale.get()+self.dvarvscalef.get()

    def setcscale(self, c):
        self.dvarcscale.set(int(c))
        self.dvarcscalef.set(round(c-int(c), 2))

    def getcscale(self):
        return self.dvarcscale.get()+self.dvarcscalef.get()
        
    def updatefields(self, forcereadall=False):
        if not forcereadall and self.ivarkeylock.get():#if user keep locked fewer data are read, otherwise all 
            data=self.dps.get(['vout', 'cout', 'pout', 'vinp', 'lock', 'prot', 'cvcc'])                     
            self.dvarvout.set(data[0])
            self.dvarcout.set(data[1])
            self.dvarpout.set(data[2])
            self.dvarvinp.set(data[3])
            self.ivarkeylock.set(data[4])
            self.setprotection(data[5])
            self.setworkmode(data[6])
            vcp=data[0:3]
            vcp.insert(TPOS, time()-self.strtme)

        else:#all data is read
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
        self.svarprot.set({0: 'none', 1: 'ovp', 2: 'ocp', 3: 'opp'}[p])

    def setworkmode(self, wm):
        self.svarwrmde.set({0: 'cv', 1: 'cc'}[wm])

if __name__=='__main__':
    from Tkinter import Tk
    root=Tk()

    try:
        root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='pwrsup.png'))
    except:
        print ('It is not possible to load the application icon')

    my_gui=DPSinterface(root)
    root.mainloop()
