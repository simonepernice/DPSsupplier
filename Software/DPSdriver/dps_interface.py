from Tkinter import Tk, Label, Button, Checkbutton, Entry, Scale, IntVar, StringVar, DoubleVar, Canvas, N, S, E, W, NORMAL, DISABLED
import tkFileDialog
from ttk import Separator

from scopetube import Scopetube
#import dps_driver

class DPSinterface:        
    def __init__(self, root):
        self.dps=None
        self.root=root
        root.title("DPS power supplier interface by Simone Pernice")

        ENTRYWIDTH=8

        row=0
        col=0
        rowspan=1
        colspan=1
        Label(root, text="Serial port: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.svardsport=StringVar()
        self.svardsport.set('/dev/ttyUSB0')        
        self.entryserport=Entry(root, textvariable=self.svardsport, width=ENTRYWIDTH)
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
        Label(root, text="Y [V/div]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvdiv=DoubleVar()
        self.dvarvdiv.set(1.0)
        self.entryydivv=Entry(root, textvariable=self.dvarvdiv, width=ENTRYWIDTH)
        self.entryydivv.grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Y [A/div]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvaradiv=DoubleVar()
        self.dvaradiv.set(1.0)
        self.entryydiva=Entry(root, textvariable=self.dvaradiv, width=ENTRYWIDTH)
        self.entryydiva.grid(row=row, column=col, sticky=W)
        
        row+=rowspan
        col=0 
        Label(root, text="X [sec/div]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarsecdiv=DoubleVar()
        self.dvarsecdiv.set(60)
        self.entryxdiv=Entry(root, textvariable=self.dvarsecdiv, width=ENTRYWIDTH)
        self.entryxdiv.grid(row=row, column=col, sticky=W)
        col+=colspan
        self.ivaracquire=IntVar()
        self.ivaracquire.set(0)        
        Checkbutton(root, variable=self.ivaracquire, text='Acquire', command=self.buttonacqaction).grid(row=row, column=col, columnspan=2, sticky=E+W)                        

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
        Label(root, text="Vout [V]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvout=DoubleVar()
        Entry(root, textvariable=self.dvarvout, state=DISABLED, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Cout [A]: ").grid(row=row, column=col, sticky=E)
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
        self.outgraph.setvdiv(1)
        self.outgraph.setcdiv(1)
        self.outgraph.settdiv(60, 0)        
        self.outgraph.drawgrid()
        self.outgraph.addpoint((2, 1, 0))
        self.outgraph.addpoint((3, 1, 60))
        self.outgraph.addpoint((4, 1, 120))
        self.outgraph.addpoint((3, 2, 180))
        self.outgraph.addpoint((2, 3, 240))
        
        row+=rowspan
        col=0
        Separator(root, orient='horizontal').grid(row=row, columnspan=4, sticky=E+W, pady=8)        

        row+=rowspan
        col=0
        rowspan=1
        colspan=2        
        Label(root, text="Vset [V]").grid(row=row, column=col, columnspan=colspan)
        col+=colspan
        Label(root, text="Cset [A]").grid(row=row, column=col, columnspan=colspan)
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
        Label(root, text="Vmax [V]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvmax=DoubleVar()
        Entry(root, textvariable=self.dvarvmax, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Cmax [A]: ").grid(row=row, column=col, sticky=E)
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
            self.entryserport.config(state=DISABLED)
            self.entrydpsadd.config(state=DISABLED)
        else:
            self.entryserport.config(state=NORMAL)
            self.entrydpsadd.config(state=NORMAL)
        print str(self.ivardpsaddr.get())
        print str(self.svardsport.get())

    def buttonacqaction(self):
        if self.ivaracquire.get():
            self.entryxdiv.config(state=DISABLED)
            self.entryydivv.config(state=DISABLED)
            self.entryydiva.config(state=DISABLED)
        else:
            self.entryxdiv.config(state=NORMAL)
            self.entryydivv.config(state=NORMAL)
            self.entryydiva.config(state=NORMAL)

    def scalevoltaction(self, event):
        print str(self.dvarvscale.get()+self.dvarvscalef.get())

    def scalecurntaction(self, event):
        print str(self.dvarcscale.get()+self.dvarcscalef.get())

    def buttonselwveaction (self):
        self.svarwave.set(tkFileDialog.askopenfilename(initialdir = ".", title = "Select wave file", filetypes = (("wave files","*.wave"),("all files","*.*"))))

root=Tk()
my_gui=DPSinterface(root)
root.mainloop()
