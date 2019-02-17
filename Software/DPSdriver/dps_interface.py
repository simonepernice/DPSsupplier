from Tkinter import Tk, Label, Button, Entry, Scale, Radiobutton, IntVar,  StringVar, DoubleVar, Canvas, N, S, E, W
import dps_driver

class DPSinterface:        
    def __init__(self, root):
        self.root = root
        root.title("DPS power supplier interface by Simone Pernice")

        row = 0
        col = 0
        rowspan = 1
        colspan = 1
        Label(root, text="Serial port").grid(row=row, column=col, sticky=E)
        col += colspan
        self.serport = StringVar()
        self.serport.set('/dev/ttyUSB0')
        Entry(root,  textvariable=self.serport).grid(row=row, column=col)        
        col += colspan
        Label(root, text="Polling time[s]").grid(row=row, column=col)
        col += colspan
        self.polltime = DoubleVar()
        self.polltime.set(1.0)
        Entry(root,  textvariable=self.polltime).grid(row=row, column=col)

        row += rowspan
        col = 0                
        Label(root, text="Model").grid(row=row, column=col, sticky=E)        
        col += colspan
        self.version = IntVar()
        self.version.set(5015)
        Entry(root,  textvariable=self.version, state="readonly").grid(row=row, column=col)
        col += colspan
        Button(root,  text='Connect', command=self.connectbutton).grid(row=row, column=col)                
        col += colspan
        self.connstat = StringVar()
        self.connstat.set("Not Connected")        
        Entry(root,  textvariable=self.connstat, state="readonly").grid(row=row, column=col)

        row += rowspan
        col = 0
        Label(root, text="Vinp [V]").grid(row=row, column=col, sticky=E)
        col += colspan
        self.vinp = DoubleVar()
        Entry(root,  textvariable=self.vinp, state='readonly').grid(row=row, column=col)
        col += colspan
        Label(root, text="Pout [W]").grid(row=row, column=col, sticky=E)
        col += colspan
        self.pout = DoubleVar()
        Entry(root,  textvariable=self.pout, state='readonly').grid(row=row, column=col)

        row += rowspan
        col = 0
        Label(root, text="Vout [V]").grid(row=row, column=col, sticky=E)
        col += colspan
        self.vout = DoubleVar()
        Entry(root,  textvariable=self.vout, state='readonly').grid(row=row, column=col)
        col += colspan
        Label(root, text="Cout [A]").grid(row=row, column=col, sticky=E)
        col += colspan
        self.cout = DoubleVar()
        Entry(root,  textvariable=self.cout, state='readonly').grid(row=row, column=col)

        row += rowspan
        col = 0
        rowspan = 4
        colspan = 5        
        self.outgraph = Canvas(root, background='white')        
        self.outgraph.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan,  sticky=E+W)

        row += rowspan
        col = 0
        rowspan = 1
        colspan = 1        
        Label(root, text="Vset [V]").grid(row=row, column=col, sticky=E)
        col += colspan
        self.vset = DoubleVar()
        Entry(root,  textvariable=self.vset).grid(row=row, column=col)
        col += colspan
        Label(root, text="Cset [A]").grid(row=row, column=col, sticky=E)
        col += 1
        self.cset = DoubleVar()
        Entry(root,  textvariable=self.cset).grid(row=row, column=col)

        row += rowspan
        colspan = 2
        col = 0       
        self.svset = DoubleVar()        
        Scale(root, from_=0, to=50, resolution=0.01, orient="horizontal").grid(row=row, column=col, columnspan=colspan, sticky=E+W)
        col += colspan
        self.scset = DoubleVar()      
        Scale(root, from_=0, to=15, resolution=0.01, orient="horizontal").grid(row=row, column=col, columnspan=colspan, sticky=E+W)

    def connectbutton(self):
        pass
root = Tk()
my_gui = DPSinterface(root)
root.mainloop()
