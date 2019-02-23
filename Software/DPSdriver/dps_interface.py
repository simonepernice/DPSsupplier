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
        Checkbutton(root, variable=self.ivarconctd, text='Connect', command=self.buttonconnectaction).grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        
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

        row+=rowspan
        col=0
        rowspan=4
        colspan=5        
        self.outgraph=Scopetube(root)
        self.outgraph.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan, sticky=E+W)
        self.outgraph.update()
        self.dvarvdiv=DoubleVar()
        self.dvarvdiv.set(1.0)        
        self.dvaradiv=DoubleVar()
        self.dvaradiv.set(1.0)
        self.dvarsdiv=DoubleVar()
        self.dvarsdiv.set(60.)
        self.dvarst0=DoubleVar()
        self.dvarst0.set(0.)
        self.outgraph.setratios(self.dvarvdiv.get(), self.dvaradiv.get(), self.dvarsdiv.get(), self.dvarst0.get())
        self.outgraph.drawgrid()
        self.outgraph.addpoint((2, 1, 1))
        self.outgraph.addpoint((3, 1, 60))
        self.outgraph.addpoint((4, 1, 120))
        self.outgraph.addpoint((3, 2, 180))
        self.outgraph.addpoint((2, 3, 240))
        print(self.outgraph.sampletime())
        print(self.outgraph.winfo_width())
        
        row+=rowspan
        rowspan=1
        colspan=1
        col=0 
        Label(root, text="Y [V/div]: ", foreground=Scopetube.VCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        e=Entry(root, textvariable=self.dvarvdiv, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.scopeupdate)
        e.grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Y [A/div]: ", foreground=Scopetube.CCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        e=Entry(root, textvariable=self.dvaradiv, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.scopeupdate)
        e.grid(row=row, column=col, sticky=W)
        row+=rowspan

        col=0
        row+=rowspan
        Label(root, text="X0 [s]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        e=Entry(root, textvariable=self.dvarst0, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.scopeupdate)
        e.grid(row=row, column=col, sticky=W)        
        col+=colspan
        Label(root, text="X [s/div]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        e=Entry(root, textvariable=self.dvarsdiv, width=ENTRYWIDTH)
        e.bind('<FocusOut>', self.scopeupdate)
        e.grid(row=row, column=col, sticky=W)

        col=2
        row+=rowspan
        self.ivaracquire=IntVar()
        self.ivaracquire.set(0)        
        Checkbutton(root, variable=self.ivaracquire, text='Acquire', command=self.buttonacqaction).grid(row=row, column=col, columnspan=2, sticky=E+W)         
        
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
        self.voltscale=Scale(root, variable=self.dvarvscale, from_=0, to=50, resolution=1, orient="horizontal")
        self.voltscale.bind("<ButtonRelease-1>", self.scalevoltaction)
        self.voltscale.grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        col+=colspan
        self.dvarcscale=DoubleVar()
        self.curntscale=Scale(root, variable=self.dvarcscale, from_=0, to=15, resolution=1, orient="horizontal")
        self.curntscale.bind("<ButtonRelease-1>", self.scalecurntaction)
        self.curntscale.grid(row=row, column=col, columnspan=colspan, sticky=E+W)

        row+=rowspan
        rowspan=1        
        colspan=2
        col=0
        self.dvarvscalef=DoubleVar()
        sc=Scale(root, variable=self.dvarvscalef, from_=0, to=0.99, resolution=0.01, orient="horizontal")
        sc.bind("<ButtonRelease-1>", self.scalevoltaction)
        sc.grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        col+=colspan
        self.dvarcscalef=DoubleVar()
        sc=Scale(root, variable=self.dvarcscalef, from_=0, to=0.99, resolution=0.01, orient="horizontal")
        sc.bind("<ButtonRelease-1>", self.scalecurntaction)
        sc.grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        
        colspan=1
        row+=rowspan
        col=0
        Label(root, text="Output mode: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.svaromode=StringVar()
        self.svaromode.set('cv')
        Entry(root, textvariable=self.svaromode, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Protection: ").grid(row=row, column=col, sticky=E)
        col+=1
        self.svarstatus=StringVar()
        self.svarstatus.set('ok')
        Entry(root, textvariable=self.svarstatus, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)

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
        Checkbutton(root, variable=self.ivaroutenab, text="Enable Output").grid(row=row, column=col, sticky=E+W, columnspan=colspan)

        row+=rowspan
        colspan=1
        col=0
        Label(root, text="Brightness: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.ivarbrght=IntVar()
        Entry(root, textvariable=self.ivarbrght, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        col+=colspan
        Button(root, text='Store', command=self.buttonconnectaction).grid(row=row, column=col, sticky=E+W, padx=8)                        
        col+=colspan
        Button(root, text='Recall', command=self.buttonconnectaction).grid(row=row, column=col, sticky=E+W, padx=8)

        row+=rowspan
        colspan=1
        col=0
        Label(root, text="Memory: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.ivarmem=IntVar()
        Entry(root, textvariable=self.ivarmem, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        col+=colspan
        colspan=2
        Button(root, text="Set Memory Active").grid(row=row, column=col, columnspan=colspan, sticky=E+W, padx=8)
        
        row+=rowspan
        col=0
        colspan=1
        Separator(root, orient='horizontal').grid(row=row, columnspan=4, sticky=E+W, pady=8)

        row+=rowspan
        col=0
        Label(root, text="Waveform: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        colspan=3
        self.svarwave=StringVar()
        Entry(root, textvariable=self.svarwave, state=DISABLED).grid(row=row, column=col, columnspan=colspan, sticky=E+W)

        row+=rowspan
        col=0
        colspan=2
        Button(root, text='Select wave', command=self.buttonselwveaction).grid(row=row, column=col, columnspan=colspan, sticky=E+W, padx=8)        
        col+=colspan
        colspan=1
        self.ivarplaywv=IntVar()
        self.ivarplaywv.set(0)        
        Checkbutton(root, variable=self.ivarplaywv, text='Play', command=self.buttonconnectaction).grid(row=row, column=col, sticky=E+W)                        
        col+=colspan
        self.ivarpausewv=IntVar()
        self.ivarpausewv.set(0)        
        Checkbutton(root, variable=self.ivarpausewv, text='Pause', command=self.buttonconnectaction).grid(row=row, column=col, sticky=E+W)
                
    def buttonconnectaction(self):
        if self.ivarconctd.get():
            try:
                self.dps=DPSdriver(self.svardpsport.get(), self.ivardpsaddr.get())
            except Exception as e:
                tkMessageBox.showerror('Error',  'Cannot connect: '+str(e))
                self.ivarconctd.set(0)
                self.dps=None
                return
            
            m=self.dps.get(['model'])
            self.ivarmodel.set(m)
            self.voltscale.config(to=m/100)
            self.curntscale.config(t0=m%100)
            self.entryserport.config(state=DISABLED)
            self.entrydpsadd.config(state=DISABLED)
        else:
            self.dps=None
            self.entryserport.config(state=NORMAL)
            self.entrydpsadd.config(state=NORMAL)

    def polling(self):
        while self.ivaracquire.get() and self.dps is not None:
            t=time()
            self.lock.aquire()
            vi=self.dps.get(['vout', 'iout'])
            vi.append(time())
            self.lock.release()            
            self.outgraph.addpoint(vi)
            self.dvarvout.set(vi[0])
            self.dvarcout.set(vi[1])
            t=(time()-t)-self.outgraph.sampletime()
            if t>0:
                sleep(t)

    def buttonacqaction(self):
        if self.ivaracquire.get():
            if self.dps is None:
                tkMessageBox.showinfo('Not connected',  'Enstablish a connection before aqcuire') 
                self.ivaracquire.set(0)
                return
            if self.threadacquire is not None and self.threadacquire.isAlive():
                self.ivaracquire.set(0)
                tkMessageBox.showwarning('Still acquiring',  'Previous acquisition session is still running, it will finish after the next sample acquisition.')
                return
            self.threadacquire=Thread(target=self.polling)
        else:
#            sleep(1.)
            if self.threadacquire is not None and self.threadacquire.isAlive():
                tkMessageBox.showinfo('Still acquiring',  'Current acquisition session will complete after the next sample') 

    def scopeupdate(self,  event):
        self.outgraph.setratios(self.dvarvdiv.get(), self.dvaradiv.get(), self.dvarsdiv.get(), self.dvarst0.get())
        self.outgraph.redraw()

    def scalevoltaction(self, event):
        if self.dps is not None:
            self.dps.set(['vset'],  [self.dvarvscale.get()+self.dvarvscalef.get()])

    def scalecurntaction(self, event):
        if self.dps is not None:
            self.dps.set(['vset'],  [self.dvarvscale.get()+self.dvarvscalef.get()])

    def buttonselwveaction (self):
        self.svarwave.set(tkFileDialog.askopenfilename(initialdir = ".", title = "Select dps file", filetypes = (("dps files","*.dps"), ("all files","*.*"))))

root=Tk()
my_gui=DPSinterface(root)
root.mainloop()
