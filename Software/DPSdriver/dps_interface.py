from Tkinter import Tk, Label, Button, Checkbutton, Entry, Scale, IntVar, StringVar, DoubleVar, Canvas, N, S, E, W, NORMAL, DISABLED
import tkFileDialog
from ttk import Separator
#import dps_driver

class DPSinterface:        
    def __init__(self, root):
        self.dps=None
        self.root=root
        root.title("DPS power supplier interface by Simone Pernice")

        row=0
        col=0
        rowspan=1
        colspan=1
        Label(root, text="Serial port: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.entryserport=Entry(root)
        self.entryserport.insert(0, '/dev/ttyUSB0')
        self.entryserport.grid(row=row, column=col, sticky=W)                
        col+=colspan
        Label(root, text="DPS address: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.entrydpsadd=Entry(root)
        self.entrydpsadd.insert(0, '1')
        self.entrydpsadd.grid(row=row, column=col, sticky=W)

        row+=rowspan
        col=0
        Label(root, text="Model: ").grid(row=row, column=col, sticky=E)        
        col+=colspan
        self.ivarvers=IntVar()
        Entry(root, textvariable=self.ivarvers, state="readonly").grid(row=row, column=col, sticky=W)
        col+=colspan
        colspan=2
        self.ivarconctd=IntVar()
        self.ivarconctd.set(0)
        Checkbutton(root, variable=self.ivarconctd, text='Connect', command=self.connectbutton).grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        
        row+=rowspan
        col=0
        colspan=1
        Separator(root, orient='horizontal').grid(row=row, columnspan=8, sticky=E+W, pady=8)
        
        row+=rowspan
        col=0
        Label(root, text="Polling time[s]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.entrypltime=Entry(root, width=6)
        self.entrypltime.insert(0, '2.0')
        self.entrypltime.grid(row=row, column=col, sticky=W)
        col+=colspan
        self.ivarpolling=IntVar()
        self.ivarpolling.set(0)        
        Checkbutton(root, variable=self.ivarpolling, text='Poll', command=self.pollingbutton).grid(row=row, column=col, columnspan=2, sticky=E+W)                        

        rowspan=1
        col=0
        row+=rowspan        
        Label(root, text="Vinp [V]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvinp=DoubleVar()
        Entry(root, textvariable=self.dvarvinp, state=DISABLED, width=6).grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Pout [W]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarpout=DoubleVar()
        Entry(root, textvariable=self.dvarpout, state=DISABLED, width=6).grid(row=row, column=col, sticky=W)

        row+=rowspan
        col=0
        Label(root, text="Vout [V]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvout=DoubleVar()
        Entry(root, textvariable=self.dvarvout, state=DISABLED, width=6).grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Cout [A]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarcout=DoubleVar()
        Entry(root, textvariable=self.dvarcout, state=DISABLED, width=6).grid(row=row, column=col, sticky=W)

        row+=rowspan
        col=0
        rowspan=4
        colspan=5        
        self.outgraph=Canvas(root, background='white')        
        self.outgraph.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan, sticky=E+W)

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
        self.voltscale=Scale(root, from_=0, to=50, resolution=0.01, orient="horizontal")
        self.voltscale.bind("<ButtonRelease-1>", self.voltsetupdate)
        self.voltscale.grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        col+=colspan
        self.curntscale=Scale(root, from_=0, to=15, resolution=0.01, orient="horizontal")
        self.curntscale.bind("<ButtonRelease-1>", self.crntsetupdate)
        self.curntscale.grid(row=row, column=col, columnspan=colspan, sticky=E+W)

        colspan=1
        row+=rowspan
        col=0
        Label(root, text="Output mode: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.svaromode=StringVar()
        self.svaromode.set('cv')
        Entry(root, textvariable=self.svaromode, width=6).grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Protection: ").grid(row=row, column=col, sticky=E)
        col+=1
        self.svarstatus=StringVar()
        self.svarstatus.set('ok')
        Entry(root, textvariable=self.svarstatus, width=6).grid(row=row, column=col, sticky=W)

        row+=rowspan
        col=0
        Separator(root, orient='horizontal').grid(row=row, columnspan=4, sticky=E+W, pady=8)

        row+=rowspan
        col=0
        Label(root, text="Vmax [V]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvmax=DoubleVar()
        Entry(root, textvariable=self.dvarvmax, width=6).grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Cmax [A]: ").grid(row=row, column=col, sticky=E)
        col+=1
        self.dvarcmax=DoubleVar()
        Entry(root, textvariable=self.dvarcmax, width=6).grid(row=row, column=col, sticky=W)
        
        row+=rowspan
        col=0
        Label(root, text="Pmax [W]: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarpmax=DoubleVar()
        Entry(root, textvariable=self.dvarpmax, width=6).grid(row=row, column=col, sticky=W)
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
        Entry(root, textvariable=self.ivarbrght, width=6).grid(row=row, column=col, sticky=W)
        col+=colspan
        Button(root, text='Store', command=self.connectbutton).grid(row=row, column=col, sticky=E+W, padx=8)                        
        col+=colspan
        Button(root, text='Recall', command=self.connectbutton).grid(row=row, column=col, sticky=E+W, padx=8)

        row+=rowspan
        colspan=1
        col=0
        Label(root, text="Memory: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.ivarmem=IntVar()
        Entry(root, textvariable=self.ivarmem, width=6).grid(row=row, column=col, sticky=W)
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
        Button(root, text='Select wave', command=self.wavefileselectionbutton).grid(row=row, column=col, columnspan=colspan, sticky=E+W, padx=8)        
        col+=colspan
        colspan=1
        self.ivarplaywv=IntVar()
        self.ivarplaywv.set(0)        
        Checkbutton(root, variable=self.ivarplaywv, text='Play', command=self.connectbutton).grid(row=row, column=col, sticky=E+W)                        
        col+=colspan
        self.ivarpausewv=IntVar()
        self.ivarpausewv.set(0)        
        Checkbutton(root, variable=self.ivarpausewv, text='Pause', command=self.connectbutton).grid(row=row, column=col, sticky=E+W)
                
    def connectbutton(self):
        if self.ivarconctd.get():
            self.entryserport.config(state=DISABLED)
            self.entrydpsadd.config(state=DISABLED)
        else:
            self.entryserport.config(state=NORMAL)
            self.entrydpsadd.config(state=NORMAL)
        print str(self.entryserport.get())
        print str(self.entrydpsadd.get())


    def pollingbutton(self):
        if self.ivarpolling.get():
            self.entrypltime.config(state=DISABLED)
        else:
            self.entrypltime.config(state=NORMAL)
        print str(self.entrypltime.get())

    def voltsetupdate(self, event):
        print str(self.voltscale.get())

    def crntsetupdate(self, event):
        print str(self.curntscale.get())

    def wavefileselectionbutton (self):
        self.svarwave.set(tkFileDialog.askopenfilename(initialdir = ".", title = "Select wave file", filetypes = (("wave files","*.wave"),("all files","*.*"))))

root=Tk()
my_gui=DPSinterface(root)
root.mainloop()
