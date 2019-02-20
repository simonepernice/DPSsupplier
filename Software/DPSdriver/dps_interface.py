from Tkinter import Tk, Label, Button, Entry, Scale, Radiobutton, IntVar, StringVar, DoubleVar, Canvas, N, S, E, W
from ttk import Separator
#import dps_driver

class DPSinterface:        
    def __init__(self, root):
        self.root = root
        root.title("DPS power supplier interface by Simone Pernice")

        row = 0
        col=0
        rowspan = 1
        colspan = 1
        Label(root, text="Serial port: ").grid(row=row, column=col, sticky=E)
        col += colspan
        self.serport = StringVar()
        self.serport.set('/dev/ttyUSB0')
        Entry(root,  textvariable=self.serport).grid(row=row, column=col, sticky=W)        
        col += colspan
        Label(root, text="DPS address: ").grid(row=row, column=col, sticky=E)
        col += colspan
        self.dpsaddress = IntVar()
        self.dpsaddress.set(1)
        Entry(root, textvariable=self.dpsaddress, width=3).grid(row=row, column=col, sticky=W)

        row += rowspan
        col=0
        Label(root, text="Model: ").grid(row=row, column=col, sticky=E)        
        col += colspan
        self.version = IntVar()
        self.version.set(5015)
        Entry(root,  textvariable=self.version, state="readonly").grid(row=row, column=col, sticky=W)
        col += colspan
        Label(root, text="Status: ").grid(row=row, column=col, sticky=E)
        col += colspan
        self.connstat = StringVar()
        self.connstat.set("Not Connected")        
        Entry(root,  textvariable=self.connstat, state="readonly").grid(row=row, column=col, sticky=W)

        row += rowspan
        col=2
        Button(root,  text='Connect', command=self.connectbutton).grid(row=row, column=col, columnspan=2, sticky=E+W)
        
        row += rowspan
        col=0
        Separator(root, orient='horizontal').grid(row=row, columnspan=8, sticky=E+W, pady=8)
        
        row += rowspan
        col=0
        Label(root, text="Polling time[s]: ").grid(row=row, column=col, sticky=E)
        col += colspan
        self.polltime = DoubleVar()
        self.polltime.set(1.0)
        Entry(root, textvariable=self.polltime, width=5).grid(row=row, column=col, sticky=W)
        col += colspan
        Button(root,  text='Run', command=self.connectbutton).grid(row=row, column=col, sticky=E+W)                        
        col += colspan
        Button(root,  text='Stop', command=self.connectbutton).grid(row=row, column=col, sticky=E+W)                        

        rowspan=1
        col=0
        row += rowspan        
        Label(root, text="Vinp [V]: ").grid(row=row, column=col, sticky=E)
        col += colspan
        self.vinp = DoubleVar()
        Entry(root, textvariable=self.vinp, state='readonly', width=5).grid(row=row, column=col, sticky=W)
        col += colspan
        Label(root, text="Pout [W]: ").grid(row=row, column=col, sticky=E)
        col += colspan
        self.pout = DoubleVar()
        Entry(root,  textvariable=self.pout, state='readonly', width=6).grid(row=row, column=col, sticky=W)

        row += rowspan
        col=0
        Label(root, text="Vout [V]: ").grid(row=row, column=col, sticky=E)
        col += colspan
        self.vout = DoubleVar()
        Entry(root,  textvariable=self.vout, state='readonly', width=5).grid(row=row, column=col, sticky=W)
        col += colspan
        Label(root, text="Cout [A]: ").grid(row=row, column=col, sticky=E)
        col += colspan
        self.cout = DoubleVar()
        Entry(root,  textvariable=self.cout, state='readonly', width=5).grid(row=row, column=col, sticky=W)

        row += rowspan
        col=0
        rowspan = 4
        colspan = 5        
        self.outgraph = Canvas(root, background='white')        
        self.outgraph.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan,  sticky=E+W)

        row += rowspan
        col=0
        rowspan = 1
        colspan = 1        
        Label(root, text="Vset [V]:").grid(row=row, column=col, sticky=E)
        col += colspan
        self.vset = DoubleVar()
        Entry(root,  textvariable=self.vset, width=5).grid(row=row, column=col, sticky=W)
        col += colspan
        Label(root, text="Cset [A]: ").grid(row=row, column=col, sticky=E)
        col += 1
        self.cset = DoubleVar()
        Entry(root, textvariable=self.cset, width=5).grid(row=row, column=col, sticky=W)

        row += rowspan
        colspan = 2
        col=0
        self.svset = DoubleVar()        
        Scale(root, label='Vset', from_=0, to=50, resolution=0.01, orient="horizontal").grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        col += colspan
        self.scset = DoubleVar()      
        Scale(root, label='Cset', from_=0, to=15, resolution=0.01, orient="horizontal").grid(row=row, column=col, columnspan=colspan, sticky=E+W)

        colspan = 1
        row += rowspan
        col=0
        Label(root, text="Output mode: ").grid(row=row, column=col, sticky=E)
        col += colspan
        self.omode = StringVar()
        self.omode.set('cv')
        Entry(root,  textvariable=self.omode, width=5).grid(row=row, column=col, sticky=W)
        col += colspan
        Label(root, text="Protection: ").grid(row=row, column=col, sticky=E)
        col += 1
        self.protection = StringVar()
        self.protection.set('none')
        Entry(root, textvariable=self.protection, width=5).grid(row=row, column=col, sticky=W)

        row += rowspan
        col=0
        Separator(root, orient='horizontal').grid(row=row, columnspan=4, sticky=E+W, pady=8)

        row += rowspan
        col=0
        Label(root, text="Vmax [V]: ").grid(row=row, column=col, sticky=E)
        col += colspan
        self.vmax = DoubleVar()
        Entry(root,  textvariable=self.vmax, width=5).grid(row=row, column=col, sticky=W)
        col += colspan
        Label(root, text="Cmax [A]: ").grid(row=row, column=col, sticky=E)
        col += 1
        self.cmax = DoubleVar()
        Entry(root, textvariable=self.cmax, width=5).grid(row=row, column=col, sticky=W)
        
        row += rowspan
        col=0
        Label(root, text="Pmax [W]: ").grid(row=row, column=col, sticky=E)
        col += colspan
        self.pmax = DoubleVar()
        Entry(root,  textvariable=self.vmax, width=6).grid(row=row, column=col, sticky=W)
        col += colspan
        Radiobutton(root, text="Enable Output", value=0, indicatoron=False).grid(row=row, column=col, sticky=E+W, columnspan=2)

        row += rowspan
        col=0
        Label(root, text="Memory: ").grid(row=row, column=col, sticky=E)
        col += colspan
        self.mem = IntVar()
        Entry(root,  textvariable=self.mem, width=2).grid(row=row, column=col, sticky=W)
        col += colspan
        Button(root,  text='Store', command=self.connectbutton).grid(row=row, column=col, sticky=E+W)                        
        col += colspan
        Button(root,  text='Recall', command=self.connectbutton).grid(row=row, column=col, sticky=E+W)

        row += rowspan
        col=0
        Separator(root, orient='horizontal').grid(row=row, columnspan=4, sticky=E+W, pady=8)

        row += rowspan
        col=0
        Label(root, text="Waveform: ").grid(row=row, column=col, sticky=E)
        col += colspan
        self.wave = StringVar()
        Entry(root,  textvariable=self.wave, state='readonly', width=15).grid(row=row, column=col, sticky=W)
        col += colspan
        Button(root,  text='Select', command=self.connectbutton).grid(row=row, column=col, columnspan=2, sticky=E+W)                                

        row += rowspan
        col=2        
        Button(root,  text='Play', command=self.connectbutton).grid(row=row, column=col, sticky=E+W)                        
        col += colspan
        Button(root,  text='Stop', command=self.connectbutton).grid(row=row, column=col, sticky=E+W)
        
    def connectbutton(self):
        pass
root = Tk()
my_gui = DPSinterface(root)
root.mainloop()
