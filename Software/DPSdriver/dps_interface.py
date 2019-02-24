from Tkinter import Tk, Label, Button, Checkbutton, Entry, Scale, IntVar, StringVar, DoubleVar, E, W, NORMAL, DISABLED
import tkMessageBox
import tkFileDialog
from ttk import Separator

from threading import Thread, Lock

from time import time, sleep

from scopetube import Scopetube
from dps_driver import DPSdriver

class DPSinterface:        
    def __init__(self, root):        
        self.root=root
        root.title("DPS power supplier interface by Simone Pernice")
        
        self.dps=None
        self.lock=Lock()
        self.threadacquire=None
        self.strtme=time()

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

        row+=rowspan
        col=0
        Label(root, text="Model: ").grid(row=row, column=col, sticky=E)        
        col+=colspan
        self.ivarmodel=IntVar()
        Entry(root, textvariable=self.ivarmodel, state="readonly", width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
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
        col=0
        row+=rowspan        
        Label(root, text="Vinp [V]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvinp=DoubleVar()
        Entry(root, textvariable=self.dvarvinp, state=DISABLED, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Pout [W]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarpout=DoubleVar()
        Entry(root, textvariable=self.dvarpout, state=DISABLED, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)

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

        colspan=1
        row+=rowspan
        col=0
        Label(root, text="Work mode: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.svarwrmde=StringVar()
        self.svarwrmde.set('cv')
        Entry(root, textvariable=self.svarwrmde, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Protection: ").grid(row=row, column=col, sticky=E)
        col+=1
        self.svarprot=StringVar()
        self.svarprot.set('ok')
        Entry(root, textvariable=self.svarprot, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)

        row+=rowspan
        col=0
        rowspan=4
        colspan=5        
        self.scopetube=Scopetube(root)
        self.scopetube.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan, sticky=E+W)
        self.scopetube.update()
        self.dvarvdiv=DoubleVar()
        self.dvarvdiv.set(1.0)        
        self.dvaradiv=DoubleVar()
        self.dvaradiv.set(1.0)
        self.dvarsdiv=DoubleVar()
        self.dvarsdiv.set(60.)
        self.dvarst0=DoubleVar()
        self.dvarst0.set(0.)
        self.scopetube.setratios(self.dvarvdiv.get(), self.dvaradiv.get(), self.dvarsdiv.get(), self.dvarst0.get())
        self.scopetube.drawgrid()
        
        row+=rowspan
        rowspan=1
        colspan=1
        col=0 
        Label(root, text="Y [V/div]: ", foreground=Scopetube.VCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        e=Entry(root, textvariable=self.dvarvdiv, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.scopeupdate)
        e.bind('<Return>', self.scopeupdate)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Y [A/div]: ", foreground=Scopetube.CCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        e=Entry(root, textvariable=self.dvaradiv, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.scopeupdate)
        e.bind('<Return>', self.scopeupdate)
        e.grid(row=row, column=col, sticky=W)
        row+=rowspan

        col=0
        row+=rowspan
        Label(root, text="X0 [s]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        e=Entry(root, textvariable=self.dvarst0, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.scopeupdate)
        e.bind('<Return>', self.scopeupdate)
        e.grid(row=row, column=col, sticky=W)        
        col+=colspan
        Label(root, text="X [s/div]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        e=Entry(root, textvariable=self.dvarsdiv, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.scopeupdate)
        e.bind('<Return>', self.scopeupdate)
        e.grid(row=row, column=col, sticky=W)

        col=0
        row+=rowspan
        Label(root, text="Rate [s/Sa]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarsecsmp=DoubleVar()
        self.dvarsecsmp.set(round(self.scopetube.sampletime(), 1))
        e=Entry(root, textvariable=self.dvarsecsmp, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.scopeupdate)
        e.bind('<Return>', self.scopeupdate)
        e.grid(row=row, column=col, sticky=W)        
        col+=colspan
        self.ivaracquire=IntVar()
        self.ivaracquire.set(0)        
        Checkbutton(root, variable=self.ivaracquire, text='Acquire', command=self.butcmdacquire).grid(row=row, column=col, columnspan=2, sticky=E+W)         
        
        row+=rowspan
        col=0
        Separator(root, orient='horizontal').grid(row=row, columnspan=4, sticky=E+W, pady=8)        

        row+=rowspan
        col=0
        rowspan=1
        colspan=2        
        Label(root, text="Vset [V]", foreground=Scopetube.VCOL).grid(row=row, column=col, columnspan=colspan)
        col+=colspan
        Label(root, text="Cset [A]", foreground=Scopetube.CCOL).grid(row=row, column=col, columnspan=colspan)
        col+=colspan

        row+=rowspan
        rowspan=1        
        colspan=2
        col=0
        self.dvarvscale=DoubleVar()
        self.voltscale=Scale(root, variable=self.dvarvscale, from_=0, to=15, resolution=1, orient="horizontal")
        self.voltscale.bind("<ButtonRelease-1>", self.sclcmdvolt)
        self.voltscale.grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        col+=colspan
        self.dvarcscale=DoubleVar()
        self.curntscale=Scale(root, variable=self.dvarcscale, from_=0, to=5, resolution=1, orient="horizontal")
        self.curntscale.bind("<ButtonRelease-1>", self.sclcmdcurrent)
        self.curntscale.grid(row=row, column=col, columnspan=colspan, sticky=E+W)

        row+=rowspan
        rowspan=1        
        colspan=2
        col=0
        self.dvarvscalef=DoubleVar()
        sc=Scale(root, variable=self.dvarvscalef, from_=0, to=0.99, resolution=0.01, orient="horizontal")
        sc.bind("<ButtonRelease-1>", self.sclcmdvolt)
        sc.grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        col+=colspan
        self.dvarcscalef=DoubleVar()
        sc=Scale(root, variable=self.dvarcscalef, from_=0, to=0.99, resolution=0.01, orient="horizontal")
        sc.bind("<ButtonRelease-1>", self.sclcmdcurrent)
        sc.grid(row=row, column=col, columnspan=colspan, sticky=E+W)

        colspan=1
        row+=rowspan
        col=0
        Label(root, text="Vmax [V]: ", foreground=Scopetube.VCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvmax=DoubleVar()
        Entry(root, textvariable=self.dvarvmax, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Cmax [A]: ", foreground=Scopetube.CCOL).grid(row=row, column=col, sticky=E)
        col+=1
        self.dvarcmax=DoubleVar()
        Entry(root, textvariable=self.dvarcmax, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        
        row+=rowspan
        col=0
        Label(root, text="Pmax [W]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarpmax=DoubleVar()
        Entry(root, textvariable=self.dvarpmax, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)       
        col+=colspan
        colspan=2
        self.ivaroutenab=IntVar()
        self.ivaroutenab.set(0)
        Checkbutton(root, variable=self.ivaroutenab, text="Out Enable", command=self.butcmdoutenable).grid(row=row, column=col, sticky=E+W, columnspan=colspan)

        row+=rowspan
        colspan=1
        col=0
        Label(root, text="Brightness: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.ivarbrght=IntVar()
        Entry(root, textvariable=self.ivarbrght, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        col+=colspan
        Button(root, text='Store', command=self.butcmdstoremem).grid(row=row, column=col, sticky=E+W, padx=8)                        
        col+=colspan
        Button(root, text='Recall', command=self.butcmdrecallmem).grid(row=row, column=col, sticky=E+W, padx=8)

        row+=rowspan
        colspan=1
        col=0
        Label(root, text="Memory: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.ivarmem=IntVar()
        Entry(root, textvariable=self.ivarmem, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        col+=colspan
        colspan=2
        Button(root, text="Activate Memory", command=self.butcmdactivemem).grid(row=row, column=col, columnspan=colspan, sticky=E+W, padx=8)
        
        row+=rowspan
        col=0
        colspan=1
        Separator(root, orient='horizontal').grid(row=row, columnspan=4, sticky=E+W, pady=8)

        row+=rowspan
        col=0
        colspan=1
        Button(root, text='Select', command=self.butcmdselwve).grid(row=row, column=col, columnspan=colspan, sticky=E+W, padx=8)
        col+=colspan
        Label(root, text="Waveform: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        colspan=2
        self.svarwave=StringVar()
        Entry(root, textvariable=self.svarwave, state=DISABLED).grid(row=row, column=col, columnspan=colspan, sticky=E+W)

        row+=rowspan
        col=0
        colspan=2
        self.ivarkeylock=IntVar()
        self.ivarkeylock.set(0)
        Checkbutton(root, variable=self.ivarkeylock, text="Key lock", command=self.butcmdkeylock).grid(row=row, column=col, sticky=E+W, columnspan=colspan)         
        col+=colspan
        colspan=1
        self.ivarplaywv=IntVar()
        self.ivarplaywv.set(0)        
        Checkbutton(root, variable=self.ivarplaywv, text='Play', command=self.butcmdplaywave).grid(row=row, column=col, sticky=E+W)                        
        col+=colspan
        self.ivarpausewv=IntVar()
        self.ivarpausewv.set(0)        
        Checkbutton(root, variable=self.ivarpausewv, text='Pause', command=self.butcmdpausewave).grid(row=row, column=col, sticky=E+W)
                
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
            
            self.ivarmem.set(0)
            self.butcmdrecallmem()
            
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
        print ('entering polling')
        while self.ivaracquire.get() and self.dps is not None:
            print ('i am polling')
            t=time()
            vi=self.updatefields()
            print 'read point '+str(vi)
            self.scopetube.addpoint(vi)
            t=self.dvarsecsmp.get()-(time()-t)
            print 'sleep for '+str(t)
            if t>0:
                sleep(t)
        print ('exiting polling')

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
            return data[0:2]+[time()-self.strtme]

        self.lock.acquire()
        data=self.dps.get(['vset', 'iset',  'vout', 'iout', 'pout', 'vinp', 'lock', 'prot', 'cvcc', 'onoff', 'bled'])
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
        return data[2:4]+[time()-self.strtme]


    def getmem(self):
        m=self.ivarmem.get()
        if m<0 or m>9:
            tkMessageBox.error('Memory location not available', 'Memory location goes from 0 to 9')
            raise ValueError('Memory location not available')        
        return m

    def memregs(self):
        mem='m'+str(self.getmem())
        return [mem+a for a in ['vset', 'iset',  'ovp', 'ocp', 'opp', 'bled', 'pre', 'onoff']]

    def butcmdrecallmem(self):
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
    
    def butcmdstoremem(self):
        if self.isconnected():
            mr=self.memregs()
            mv=[
                self.getvscale(), 
                self.getcscale(), 
                self.dvarvmax.get(), 
                self.dvarcmax.get(), 
                self.dvarpmax.get(), 
                self.ivarbrght.get(), 
                0, 
                self.ivaroutenab.get()
            ]
            self.lock.acquire()
            self.dps.set(mr, mv)
            self.lock.release()
    
    def butcmdactivemem(self):
        if self.isconnected():
            m=self.getmem()
            self.lock.acquire()
            self.dps.set(['mset'], [m])
            self.lock.release()
            self.ivarmem.set(0)
            self.butcmdrecallmem()

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

    def scopeupdate(self,  event):
        self.scopetube.setratios(self.dvarvdiv.get(), self.dvaradiv.get(), self.dvarsdiv.get(), self.dvarst0.get())
        self.scopetube.redraw()

    def sclcmdvolt(self, event):
        if self.isconnected():
            self.lock.acquire()
            self.dps.set(['vset'],  [self.getvscale()])
            self.lock.release()

    def sclcmdcurrent(self, event):
        if self.isconnected():
            self.lock.acquire()
            self.dps.set(['iset'],  [self.getcscale()])
            self.lock.release()

    def butcmdselwve (self):
        self.svarwave.set(tkFileDialog.askopenfilename(initialdir = ".", title = "Select dps file", filetypes = (("dps files","*.dps"), ("all files","*.*"))))

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
    
root=Tk()
my_gui=DPSinterface(root)
root.mainloop()
