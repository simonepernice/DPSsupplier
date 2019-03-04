from Tkinter import Label, Checkbutton, Entry, Scale, IntVar, StringVar, DoubleVar, E, W, NORMAL, DISABLED, Menu, Toplevel, PhotoImage
import tkMessageBox
import tkFileDialog
from ttk import Separator

from threading import Thread, Lock

from time import time, sleep

from scopetube import Scopetube
from dps_driver import DPSdriver
from mem_interface import Meminterface

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
        wavemenu.add_command(label="Edit wave...", command=self.toimplement)
        wavemenu.add_command(label="Save wave as...", command=self.toimplement)
        menubar.add_cascade(label="Wave", menu=wavemenu)
 
        memmenu=Menu(menubar, tearoff=0)
        memmenu .add_command(label="Edit...", command=self.mnucmdedtmem)
        menubar.add_cascade(label="Memory", menu=memmenu)
  
        helpmenu=Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", command=self.toimplement)
        helpmenu.add_command(label="About...", command=self.toimplement)
        menubar.add_cascade(label="Help", menu=helpmenu)

        root.config(menu=menubar)

        ENTRYWIDTH=10

        row=0
        col=0
        rowspan=1
        colspan=1
        Label(root, text="Serial port: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.svardpsport=StringVar()
        self.svardpsport.set('/dev/ttyUSB0')        
        self.entryserport=Entry(root, textvariable=self.svardpsport, width=ENTRYWIDTH)
        self.entryserport.grid(row=row, column=col, sticky=W)                
        col+=colspan
        Label(root, text="DPS address: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.ivardpsaddr=IntVar()
        self.ivardpsaddr.set(1)
        self.entrydpsadd=Entry(root, textvariable=self.ivardpsaddr, width=ENTRYWIDTH)
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

        rowspan=1
        colspan=1
        col=0
        row+=rowspan        
        Label(root, text="Vinp [V]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvinp=DoubleVar()
        Entry(root, textvariable=self.dvarvinp, state=DISABLED, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        col+=colspan
        colspan=2
        self.ivarkeylock=IntVar()
        self.ivarkeylock.set(0)
        Checkbutton(root, variable=self.ivarkeylock, text="KeyLock", command=self.butcmdkeylock).grid(row=row, column=col, sticky=E+W, columnspan=colspan)         
        col+=colspan        
        self.ivaroutenab=IntVar()
        self.ivaroutenab.set(0)
        Checkbutton(root, variable=self.ivaroutenab, text="OutEnab", command=self.butcmdoutenable).grid(row=row, column=col, sticky=E+W, columnspan=colspan)    

        row+=rowspan
        colspan=1
        col=0
        Label(root, text="Model: ").grid(row=row, column=col, sticky=E)        
        col+=colspan
        self.ivarmodel=IntVar()
        Entry(root, textvariable=self.ivarmodel, state="readonly", width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)        
        col+=colspan
        Label(root, text="Work mode: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.svarwrmde=StringVar()
        self.svarwrmde.set('cv')
        Entry(root, textvariable=self.svarwrmde, state=DISABLED, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Protection: ").grid(row=row, column=col, sticky=E)        
        col+=1
        self.svarprot=StringVar()
        self.svarprot.set('ok')
        Entry(root, textvariable=self.svarprot, state=DISABLED, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)

        colspan=1
        row+=rowspan
        col=0
        Label(root, text="Vmax [V]: ", foreground=Scopetube.VCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvmaxm0=DoubleVar()
        e=Entry(root, textvariable=self.dvarvmaxm0, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.wrtdvarvmaxm0)
        e.bind('<Return>', self.wrtdvarvmaxm0)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Cmax [A]: ", foreground=Scopetube.CCOL).grid(row=row, column=col, sticky=E)
        col+=1
        self.dvarcmaxm0=DoubleVar()
        Entry(root, textvariable=self.dvarcmaxm0, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Pmax [W]: ", foreground=Scopetube.PCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarpmaxm0=DoubleVar()
        Entry(root, textvariable=self.dvarpmaxm0, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)           

        row+=rowspan
        col=0
        Label(root, text="Vout [V]: ", foreground=Scopetube.VCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvout=DoubleVar()
        Entry(root, textvariable=self.dvarvout, state=DISABLED, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Cout [A]: ", foreground=Scopetube.CCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarcout=DoubleVar()
        Entry(root, textvariable=self.dvarcout, state=DISABLED, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Pout [W]: ", foreground=Scopetube.PCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarpout=DoubleVar()
        Entry(root, textvariable=self.dvarpout, state=DISABLED, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)        

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
        Label(root, text="Y [V/div]: ", foreground=Scopetube.VCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvdiv=DoubleVar()
        self.dvarvdiv.set(1.)          
        e=Entry(root, textvariable=self.dvarvdiv, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.scopeupdate)
        e.bind('<Return>', self.scopeupdate)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Y [A/div]: ", foreground=Scopetube.CCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarcdiv=DoubleVar()
        self.dvarcdiv.set(1.)        
        e=Entry(root, textvariable=self.dvarcdiv, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.scopeupdate)
        e.bind('<Return>', self.scopeupdate)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Y [W/div]: ", foreground=Scopetube.PCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarpdiv=DoubleVar()
        self.dvarpdiv.set(1.)          
        e=Entry(root, textvariable=self.dvarpdiv, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.scopeupdate)
        e.bind('<Return>', self.scopeupdate)
        e.grid(row=row, column=col, sticky=W)

        row+=rowspan
        rowspan=1
        colspan=1
        col=0 
        Label(root, text="Y0 [V]: ", foreground=Scopetube.VCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarv0=DoubleVar()
        self.dvarv0.set(0.)          
        e=Entry(root, textvariable=self.dvarv0, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.scopeupdate)
        e.bind('<Return>', self.scopeupdate)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Y0 [A]: ", foreground=Scopetube.CCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarc0=DoubleVar()
        self.dvarc0.set(0.)        
        e=Entry(root, textvariable=self.dvarc0, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.scopeupdate)
        e.bind('<Return>', self.scopeupdate)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Y0 [W]: ", foreground=Scopetube.PCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarp0=DoubleVar()
        self.dvarp0.set(0.)          
        e=Entry(root, textvariable=self.dvarp0, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.scopeupdate)
        e.bind('<Return>', self.scopeupdate)
        e.grid(row=row, column=col, sticky=W)

        row+=rowspan
        rowspan=1
        colspan=2
        col=0
        self.ivarvena=IntVar()
        self.ivarvena.set(1)        
        Checkbutton(root, variable=self.ivarvena, text='Voltage show', foreground=Scopetube.VCOL, command=self.scopeupdate).grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        col+=colspan
        self.ivarcena=IntVar()
        self.ivarcena.set(1)        
        Checkbutton(root, variable=self.ivarcena, text='Current show', foreground=Scopetube.CCOL, command=self.scopeupdate).grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        col+=colspan
        self.ivarpena=IntVar()
        self.ivarpena.set(1)        
        Checkbutton(root, variable=self.ivarpena, text='Power show', foreground=Scopetube.PCOL, command=self.scopeupdate).grid(row=row, column=col, columnspan=colspan, sticky=E+W)

        row+=rowspan
        col=0
        colspan=1
        rowspan=1
        Label(root, text="X [s/div]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarsdiv=DoubleVar()
        self.dvarsdiv.set(60.)        
        e=Entry(root, textvariable=self.dvarsdiv, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.scopeupdate)
        e.bind('<Return>', self.scopeupdate)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan        
        Label(root, text="X0 [s]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvars0=DoubleVar()
        self.dvars0.set(0.)        
        e=Entry(root, textvariable=self.dvars0, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.scopeupdate)
        e.bind('<Return>', self.scopeupdate)
        e.grid(row=row, column=col, sticky=W)        
        col+=colspan
        Label(root, text="Rate [s/Sa]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarsecsmp=DoubleVar()        
        e=Entry(root, textvariable=self.dvarsecsmp, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.scopeupdate)
        e.bind('<Return>', self.scopeupdate)
        e.grid(row=row, column=col, sticky=W)

        row+=rowspan
        col=0
        colspan=2
        self.ivarmem=IntVar()
        sc=Scale(root, label='Recall memory', variable=self.ivarmem, from_=0, to=9, resolution=1, orient="horizontal")
        sc.bind("<ButtonRelease-1>", self.sclcmdrecallmem)
        sc.grid(row=row, column=col, columnspan=colspan)#, sticky=W+E
        col+=colspan
        self.ivarbrghtness=IntVar()
        sc=Scale(root, label='Brightness', variable=self.ivarbrghtness, from_=0, to=5, resolution=1, orient="horizontal")
        sc.bind("<ButtonRelease-1>", self.sclcmdrecallmem)
        sc.grid(row=row, column=col, columnspan=colspan)#, sticky=W+E        
        col+=colspan
        self.ivaracquire=IntVar()
        self.ivaracquire.set(0)        
        Checkbutton(root, variable=self.ivaracquire, text='Run acquisition', command=self.butcmdacquire).grid(row=row, column=col, columnspan=2, sticky=E+W)               

        row+=rowspan
        rowspan=1        
        colspan=3
        col=0
        self.dvarvscale=DoubleVar()
        self.voltscale=Scale(root, label='Vset[V]', foreground=Scopetube.VCOL, variable=self.dvarvscale, from_=0, to=15, resolution=1, orient="horizontal")
        self.voltscale.bind("<ButtonRelease-1>", self.sclcmdvolt)
        self.voltscale.grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        col+=colspan
        self.dvarcscale=DoubleVar()
        self.curntscale=Scale(root,label='Cset[A]', foreground=Scopetube.CCOL, variable=self.dvarcscale, from_=0, to=5, resolution=1, orient="horizontal")
        self.curntscale.bind("<ButtonRelease-1>", self.sclcmdcurrent)
        self.curntscale.grid(row=row, column=col, columnspan=colspan, sticky=E+W)

        row+=rowspan
        rowspan=1        
        col=0
        self.dvarvscalef=DoubleVar()
        sc=Scale(root, foreground=Scopetube.VCOL, variable=self.dvarvscalef, from_=0, to=0.99, resolution=0.01, orient="horizontal")
        sc.bind("<ButtonRelease-1>", self.sclcmdvolt)
        sc.grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        col+=colspan
        self.dvarcscalef=DoubleVar()
        sc=Scale(root, foreground=Scopetube.CCOL, variable=self.dvarcscalef, from_=0, to=0.99, resolution=0.01, orient="horizontal")
        sc.bind("<ButtonRelease-1>", self.sclcmdcurrent)
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
        Entry(root, textvariable=self.svarwave, width=ENTRYWIDTH, state=DISABLED).grid(row=row, column=col, columnspan=colspan, sticky=E+W)
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
        self.scopeupdate(None) 
        self.dvarsecsmp.set(round(self.scopetube.sampletime(), 1))
        self.scopetube.addpoint((5, 0., 0., 0.))
        self.scopetube.addpoint((4.5, 0.5, 2.25, 1.))
        self.scopetube.addpoint((4.0, 1.0, 4.0, 2.))
        self.scopetube.addpoint((3.9, 1.5, 5.35, 3.))
        self.scopetube.addpoint((3.0, 2.0, 6., 4.))
        self.scopetube.addpoint((3.5, 1.8, 3.5*1.8, 5.))
        self.scopetube.addpoint((3.8, 1.7, 3.8*1.7, 6.))
        
    def butcmdconnect(self):
        if self.ivarconctd.get():
            try:
                self.dps=DPSdriver(self.svardpsport.get(), self.ivardpsaddr.get())
            except Exception as e:
                tkMessageBox.showerror('Error',  'Cannot connect: '+str(e))
                self.ivarconctd.set(0)
                self.dps=None
                return
            
            m=self.dps.get(['model'])[0]
            self.ivarmodel.set(m)
            self.voltscale.config(to=m/100)
            self.curntscale.config(to=m%100)            

            self.ivarkeylock.set(0) #otherwise update fields does not read all
            self.updatefields()
            self.ivarkeylock.set(1)
            self.butcmdkeylock()
            
            self.entryserport.config(state=DISABLED)
            self.entrydpsadd.config(state=DISABLED)
        else:
            self.dps=None
            self.entryserport.config(state=NORMAL)
            self.entrydpsadd.config(state=NORMAL)

    def polling(self):
#        print ('entering polling')
        while self.ivaracquire.get() and self.dps is not None:
#            print ('i am polling')
            t=time()
            vip=self.updatefields()
#            print 'read point '+str(vi)
            self.scopetube.addpoint(vip)
            t=self.dvarsecsmp.get()-(time()-t)
#            print 'sleep for '+str(t)
            if t>0:
                sleep(t)
#        print ('exiting polling')

    def setvscale(self, v):
        self.dvarvscale.set(int(v))
        self.dvarvscalef.set(round(v-int(v), 2))

    def getvscale(self):
        return self.dvarvscale.get()+self.dvarvscalef.get()

    def getcscale(self):
        return self.dvarcscale.get()+self.dvarcscalef.get()

    def setcscale(self, c):
        self.dvarcscale.set(int(c))
        self.dvarcscalef.set(round(c-int(c), 2))
        
    def updatefields(self):
        if self.ivarkeylock.get():#if user keep locked only few datas are read, otherwise all 
            self.lock.acquire()
            data=self.dps.get(['vout', 'iout', 'pout', 'vinp', 'lock', 'prot', 'cvcc'])
            self.lock.release()                      
            self.dvarvout.set(data[0])
            self.dvarcout.set(data[1])
            self.dvarpout.set(data[2])
            self.dvarvinp.set(data[3])
            self.ivarkeylock.set(data[4])
            self.svarprot.set({0: 'ok', 1: 'ovp', 2: 'ocp', 3: 'opp'}[data[5]])
            self.svarwrmde.set({0: 'cv', 1: 'cc'}[data[6]])
            return data[0:3]+[time()-self.strtme]

        self.lock.acquire()
        data=self.dps.get(['vset', 'cset',  'vout', 'iout', 'pout', 'vinp', 'lock', 'prot', 'cvcc', 'onoff', 'bled'])
        self.lock.release()
        self.setvscale(data[0])
        self.setcscale(data[1])
        self.dvarvout.set(data[2])
        self.dvarcout.set(data[3])
        self.dvarpout.set(data[4])
        self.dvarvinp.set(data[5])
        self.ivarkeylock.set(data[6])
        self.svarprot.set({0: 'ok', 1: 'ovp', 2: 'ocp', 3: 'opp'}[data[7]])
        self.svarwrmde.set({0: 'cv', 1: 'cc'}[data[8]])
        self.ivaroutenab.set(data[9])
        return data[2:5]+[time()-self.strtme]

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

    def scopeupdate(self,  *event):
        self.scopetube.setratios(
            self.dvarvdiv.get(), self.dvarv0.get(), self.ivarvena.get(),
            self.dvarcdiv.get(), self.dvarc0.get(), self.ivarcena.get(),  
            self.dvarpdiv.get(), self.dvarp0.get(), self.ivarpena.get(),  
            self.dvarsdiv.get(), self.dvars0.get()
        )
        self.scopetube.redraw()

    def sclcmdvolt(self, event):
        if self.isconnected():
            self.lock.acquire()
            self.dps.set(['vset'],  [self.getvscale()])
            self.lock.release()

    def sclcmdcurrent(self, event):
        if self.isconnected():
            self.lock.acquire()
            self.dps.set(['cset'],  [self.getcscale()])
            self.lock.release()

    def mnucmdselwve (self):
        self.svarwave.set(tkFileDialog.askopenfilename(initialdir=".", title="Select dps file", filetypes=(("dps files","*.dps"), ("all files","*.*"))))

    def mnucmdload (self):
        self.scopetube.load(tkFileDialog.askopenfilename(initialdir=".", title="Select point file", filetypes=(("csv files","*.csv"), ("all files","*.*"))))

    def mnucmdsave(self):
        self.scopetube.save(tkFileDialog.asksaveasfilename(initialdir=".", title="Select dps file", filetypes=(("csv files","*.csv"), ("all files","*.*"))))

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
        
    def wrtdvarvmaxm0(self,  a):
        print 'vmax is changed '+str(a)

    def toimplement(self):
        pass
        
    def mnucmdedtmem(self):
        tl=Toplevel(self.root)
        tl.tk.call('wm', 'iconphoto', tl._w, PhotoImage(file='./pwrsup.png'))        
        tl.focus_force()
        tl.grab_set()
        Meminterface(tl, self.dps, self.lock)
    
    def sclcmdrecallmem(self, event):
        if self.isconnected():
            mr=self.memregs()
            self.lock.acquire()
            data=self.dps.get(mr)
            self.lock.release()
            self.setvscale(data[0])
            self.setcscale(data[1])
            self.dvarvmax.set(data[2])
            self.dvarcmax.set(data[3])
            self.dvarpmax.set(data[4])
            self.ivarbrght.set(data[5])
            self.ivaroutenab.set(data[7])
