from Tkinter import Label, Checkbutton, Entry, Scale, IntVar, StringVar, DoubleVar, E, W, NORMAL, Menu, Toplevel, PhotoImage
import tkMessageBox
import tkFileDialog
from ttk import Separator

from threading import Thread, Lock

from time import time, sleep

from scopetube import Scopetube
from dps_driver import DPSdriver
from mem_interface import Meminterface
from wve_interface import Wveinterface
from constants import ENTRYWIDTH, VCOL, CCOL, PCOL, TPOS
from dpsfile import Dpsfile

class DPSinterface:        
    def __init__(self, root):        
        self.root=root
        root.title("DPS power supplier interface by Simone Pernice")
        
        self.dps=None
        self.lock=Lock()
        self.threadacquire=None
        self.strtme=time()
        
        menubar=Menu(root)
        
        filemenu=Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        scopemenu=Menu(menubar, tearoff=0)
        scopemenu .add_command(label="Load sampled points...", command=self.mnucmdload)
        scopemenu .add_command(label="Save sampled points as...", command=self.mnucmdsave)
        menubar.add_cascade(label="Scope", menu=scopemenu)
        
        wavemenu=Menu(menubar, tearoff=0)
        wavemenu.add_command(label="Load wave...", command=self.mnucmdselwve)
        wavemenu.add_command(label="Edit wave...", command=self.mnucmdedtwve)
        wavemenu.add_command(label="Save wave as...", command=self.toimplement)
        menubar.add_cascade(label="Wave", menu=wavemenu)
 
        memmenu=Menu(menubar, tearoff=0)
        memmenu .add_command(label="Edit memories...", command=self.mnucmdedtmem)
        menubar.add_cascade(label="Memory", menu=memmenu)
  
        helpmenu=Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", command=self.toimplement)
        helpmenu.add_command(label="About...", command=self.toimplement)
        menubar.add_cascade(label="Help", menu=helpmenu)

        root.config(menu=menubar)

        row=0
        col=0
        rowspan=1
        colspan=1
        Label(root, text="Serial port: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.svardpsport=StringVar()
        self.svardpsport.set('/dev/ttyUSB0')        
        self.entryserport=Entry(root, textvariable=self.svardpsport, width=ENTRYWIDTH, justify='right')
        self.entryserport.grid(row=row, column=col, sticky=W)                
        col+=colspan
        Label(root, text="DPS address: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.ivardpsaddr=IntVar()
        self.ivardpsaddr.set(1)
        self.entrydpsadd=Entry(root, textvariable=self.ivardpsaddr, width=ENTRYWIDTH, justify='right')
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
        s.bind("<ButtonRelease-1>", self.entbndbrghtnss)
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
        s=Scale(root, label='Mem Recall', variable=self.ivarsetmem, from_=0, to=9, resolution=1, orient="horizontal")
        s.bind("<ButtonRelease-1>", self.entbndmemory)
        s.grid(row=row, column=col, columnspan=colspan, sticky=E+W)
  
        row+=rowspan
        colspan=1
        col=0
        Label(root, text="Vinp [V]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvinp=DoubleVar()
        Entry(root, textvariable=self.dvarvinp, state='readonly', width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)       
        col+=colspan
        Label(root, text="Out Mode: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.svarwrmde=StringVar()
        self.setworkmode(0)
        Entry(root, textvariable=self.svarwrmde, state='readonly', width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Protection: ").grid(row=row, column=col, sticky=E)        
        col+=1
        self.svarprot=StringVar()
        self.setprotection(0)
        Entry(root, textvariable=self.svarprot, state='readonly', width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)

        colspan=1
        row+=rowspan
        col=0
        Label(root, text="Vmax [V]: ", foreground=VCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvmaxm0=DoubleVar()
        e=Entry(root, textvariable=self.dvarvmaxm0, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndvmax)
        e.bind('<Return>', self.entbndvmax)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Cmax [A]: ", foreground=CCOL).grid(row=row, column=col, sticky=E)
        col+=1
        self.dvarcmaxm0=DoubleVar()
        e=Entry(root, textvariable=self.dvarcmaxm0, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndcmax)
        e.bind('<Return>', self.entbndcmax)        
        e.grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Pmax [W]: ", foreground=PCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarpmaxm0=DoubleVar()
        e=Entry(root, textvariable=self.dvarpmaxm0, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndpmax)
        e.bind('<Return>', self.entbndpmax)
        e.grid(row=row, column=col, sticky=W)           

        row+=rowspan
        col=0
        Label(root, text="Vout [V]: ", foreground=VCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvout=DoubleVar()
        Entry(root, textvariable=self.dvarvout, state='readonly', width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Cout [A]: ", foreground=CCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarcout=DoubleVar()
        Entry(root, textvariable=self.dvarcout, state='readonly', width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Pout [W]: ", foreground=PCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarpout=DoubleVar()
        Entry(root, textvariable=self.dvarpout, state='readonly', width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)        

        row+=rowspan
        col=0
        rowspan=6
        colspan=6        
        self.scopetube=Scopetube(root)
        self.scopetube.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan, sticky=E+W)
        
        row+=rowspan
        rowspan=1
        colspan=1
        col=0 
        Label(root, text="Y [V/div]: ", foreground=VCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvdiv=DoubleVar()
        self.dvarvdiv.set(1.)          
        e=Entry(root, textvariable=self.dvarvdiv, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
        e.bind('<Return>', self.entbndcmdbutscpupdt)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Y [A/div]: ", foreground=CCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarcdiv=DoubleVar()
        self.dvarcdiv.set(1.)        
        e=Entry(root, textvariable=self.dvarcdiv, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
        e.bind('<Return>', self.entbndcmdbutscpupdt)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Y [W/div]: ", foreground=PCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarpdiv=DoubleVar()
        self.dvarpdiv.set(1.)          
        e=Entry(root, textvariable=self.dvarpdiv, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
        e.bind('<Return>', self.entbndcmdbutscpupdt)
        e.grid(row=row, column=col, sticky=W)

        row+=rowspan
        rowspan=1
        colspan=1
        col=0 
        Label(root, text="Y0 [V]: ", foreground=VCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarv0=DoubleVar()
        self.dvarv0.set(0.)          
        e=Entry(root, textvariable=self.dvarv0, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
        e.bind('<Return>', self.entbndcmdbutscpupdt)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Y0 [A]: ", foreground=CCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarc0=DoubleVar()
        self.dvarc0.set(0.)        
        e=Entry(root, textvariable=self.dvarc0, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
        e.bind('<Return>', self.entbndcmdbutscpupdt)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Y0 [W]: ", foreground=PCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarp0=DoubleVar()
        self.dvarp0.set(0.)          
        e=Entry(root, textvariable=self.dvarp0, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
        e.bind('<Return>', self.entbndcmdbutscpupdt)
        e.grid(row=row, column=col, sticky=W)

        row+=rowspan
        rowspan=1
        colspan=2
        col=0
        self.ivarvena=IntVar()
        self.ivarvena.set(1)        
        Checkbutton(root, variable=self.ivarvena, text='Voltage show', foreground=VCOL, command=self.entbndcmdbutscpupdt).grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        col+=colspan
        self.ivarcena=IntVar()
        self.ivarcena.set(1)        
        Checkbutton(root, variable=self.ivarcena, text='Current show', foreground=CCOL, command=self.entbndcmdbutscpupdt).grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        col+=colspan
        self.ivarpena=IntVar()
        self.ivarpena.set(1)        
        Checkbutton(root, variable=self.ivarpena, text='Power show', foreground=PCOL, command=self.entbndcmdbutscpupdt).grid(row=row, column=col, columnspan=colspan, sticky=E+W)

        row+=rowspan
        col=0
        colspan=1
        rowspan=1
        Label(root, text="X [s/div]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarsdiv=DoubleVar()
        self.dvarsdiv.set(60.)        
        e=Entry(root, textvariable=self.dvarsdiv, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
        e.bind('<Return>', self.entbndcmdbutscpupdt)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan        
        Label(root, text="X0 [s]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvars0=DoubleVar()
        self.dvars0.set(0.)        
        e=Entry(root, textvariable=self.dvars0, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
        e.bind('<Return>', self.entbndcmdbutscpupdt)
        e.grid(row=row, column=col, sticky=W)        
        col+=colspan
        Label(root, text="S.Rate[s/Sa]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarsecsmp=DoubleVar()        
        e=Entry(root, textvariable=self.dvarsecsmp, width=ENTRYWIDTH, justify='right')
        e.bind('<FocusOut>', self.entbndcmdbutscpupdt)
        e.bind('<Return>', self.entbndcmdbutscpupdt)
        e.grid(row=row, column=col, sticky=W)

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

        self.scopetube.update()
        self.entbndcmdbutscpupdt(None) 
        self.dvarsecsmp.set(round(self.scopetube.sampletime(), 1))
        
    def butcmdconnect(self):
        if self.ivarconctd.get():
            try:
                self.dps=DPSdriver(self.svardpsport.get(), self.ivardpsaddr.get())
            except Exception as e:
                tkMessageBox.showerror('Error',  'Cannot connect: '+str(e))
                self.ivarconctd.set(0)
                self.dps=None
                return
            
            m=self.dps.get(['model', 'fware'])
            self.ivarfwver.set(m[1])
            m=m[0]
            self.ivarmodel.set(m)
            self.voltscale.config(to=m/100)
            self.curntscale.config(to=m%100)            

            self.ivarkeylock.set(0) #otherwise update fields does not read all
            self.updatefields()
            self.ivarkeylock.set(1)
            self.butcmdkeylock()
            
            self.entryserport.config(state='readonly')
            self.entrydpsadd.config(state='readonly')
        else:
            self.dps=None
            self.entryserport.config(state=NORMAL)
            self.entrydpsadd.config(state=NORMAL)

    def polling(self):
        while self.ivaracquire.get() and self.dps is not None:
            t=time()
            vip=self.updatefields()
            self.scopetube.addpoint(vip)
            t=self.dvarsecsmp.get()-(time()-t)
            if t>0:
                sleep(t)

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
            self.lock.acquire()
            data=self.dps.get(['vout', 'cout', 'pout', 'vinp', 'lock', 'prot', 'cvcc'])
            self.lock.release()                      
            self.dvarvout.set(data[0])
            self.dvarcout.set(data[1])
            self.dvarpout.set(data[2])
            self.dvarvinp.set(data[3])
            self.ivarkeylock.set(data[4])
            self.setprotection(data[5])
            self.setworkmode(data[6])
            vcp=data[0:3]
            vcp.insert(TPOS, time()-self.strtme)
            return vcp

        self.lock.acquire()
        data=self.dps.get(['vset', 'cset',  'vout', 'cout', 'pout', 'vinp', 'lock', 'prot', 'cvcc', 'onoff', 'brght', 'mset'])
        self.lock.release()
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
        vcp=data[2:5]
        vcp.insert(TPOS, time()-self.strtme)
        return vcp        

    def setprotection(self, p):
        self.svarprot.set({0: 'none', 1: 'ovp', 2: 'ocp', 3: 'opp'}[p])

    def setworkmode(self, wm):
        self.svarwrmde.set({0: 'cv', 1: 'cc'}[wm])

    def butcmdacquire(self):
        if self.ivaracquire.get():
            if not self.isconnected():
                self.ivaracquire.set(0)
                return
            if self.threadacquire is not None and self.threadacquire.isAlive():
                self.ivaracquire.set(0)
                tkMessageBox.showwarning('Still acquiring',  'Previous acquisition session is still running, it will finish after the next sample acquisition.')
                return
            self.scopetube.resetpoints()
            self.strtme=time()
            self.threadacquire=Thread(target=self.polling)
            self.threadacquire.start()
        else:
            if self.threadacquire is not None and self.threadacquire.isAlive():
                tkMessageBox.showinfo('Still acquiring',  'Current acquisition session will complete after the next sample') 

    def entbndcmdbutscpupdt(self,  *event):
        self.scopetube.setratios(
            self.dvarvdiv.get(), self.dvarv0.get(), self.ivarvena.get(),
            self.dvarcdiv.get(), self.dvarc0.get(), self.ivarcena.get(),  
            self.dvarpdiv.get(), self.dvarp0.get(), self.ivarpena.get(),  
            self.dvarsdiv.get(), self.dvars0.get()
        )
        self.scopetube.redraw()

    def sclbndvolt(self, event):
        if self.isconnected():
            self.lock.acquire()
            self.dps.set(['vset'],  [self.getvscale()])
            self.lock.release()

    def sclbndcrnt(self, event):
        if self.isconnected():
            self.lock.acquire()
            self.dps.set(['cset'],  [self.getcscale()])
            self.lock.release()

    def mnucmdselwve (self):
        fname=tkFileDialog.askopenfilename(initialdir=".", title="Select dps file", filetypes=(("dps files","*.dps"), ("all files","*.*")))
        if fname:
            self.svarwave.set(fname)
            self.dpsfwave=Dpsfile()
            self.dpsfwave.load(fname)

    def mnucmdload (self):
        fname=tkFileDialog.askopenfilename(initialdir=".", title="Select point file", filetypes=(("dps files","*.dps"), ("all files","*.*")))
        if fname:
            self.scopetube.load(fname)

    def mnucmdsave(self):
        fname=tkFileDialog.asksaveasfilename(initialdir=".", title="Select dps file", filetypes=(("dps files","*.dps"), ("all files","*.*")))
        if fname:
            self.scopetube.save(fname)

    def butcmdkeylock(self):
        if self.isconnected():
            self.lock.acquire()
            self.dps.set(['lock'], [self.ivarkeylock.get()])
            self.lock.release()
        else:
            self.ivarkeylock.set(0)

    def butcmdoutenable(self):
        if self.isconnected():
            self.lock.acquire()
            self.dps.set(['onoff'], [self.ivaroutenab.get()])
            self.lock.release()
        else:
            self.ivaroutenab.set(0)

    def isconnected(self):
        if self.dps is None:
            tkMessageBox.showinfo('Not connected',  'Enstablish a connection before') 
            return False
        return True

    def butcmdplaywave(self):
        pass
        
    def butcmdpausewave(self):
        pass

    def toimplement(self):
        pass
        
    def mnucmdedtmem(self):
        tl=Toplevel(self.root)
        tl.tk.call('wm', 'iconphoto', tl._w, PhotoImage(file='./pwrsup.png'))        
        tl.focus_force()
        tl.grab_set()
        Meminterface(tl, self.dps, self.lock)

    def mnucmdedtwve(self):
        if self.dpsfwave is not None:
            tl=Toplevel(self.root)
            tl.tk.call('wm', 'iconphoto', tl._w, PhotoImage(file='./pwrsup.png'))        
            tl.focus_force()
            tl.grab_set()
            Wveinterface(tl, self.dpsfwave)

    def entbndmemory(self, event):
        if self.isconnected():            
            m=self.ivarsetmem.get()
            self.lock.acquire()
            self.dps.set(['mset'], [m])
            self.lock.release()
            self.updatefields(True)
            #self.ivarsetmem.set(0) #not sure that is required because the active memory is always 0, when a different is set, it is actually copied on 0

    def entbndbrghtnss(self, event):
        if self.isconnected():            
            b=self.ivarbrghtnes.get()
            self.lock.acquire()
            self.dps.set(['brght'], [b])
            self.lock.release()
    
    def entbndvmax(self, event):
        if self.isconnected():
            self.lock.acquire()
            self.dps.set(['m0vmax'], [self.dvarvmaxm0.get()])
            self.lock.release()            

    def entbndcmax(self, event):
        if self.isconnected():
            self.lock.acquire()
            self.dps.set(['m0cmax'], [self.dvarcmaxm0.get()])
            self.lock.release()

    def entbndpmax(self, event):
        if self.isconnected():
            self.lock.acquire()
            self.dps.set(['m0pmax'], [self.dvarpmaxm0.get()])
            self.lock.release()  

if __name__=='__main__':
    from Tkinter import Tk
    root=Tk()

    root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='.\\pwrsup.png'))

    my_gui=DPSinterface(root)
    root.mainloop()
