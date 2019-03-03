from Tkinter import Label, Button, Checkbutton, Entry, Scale, IntVar, DoubleVar, E, W
import tkMessageBox

from scopetube import Scopetube

class Meminterface:        
    def __init__(self, root,  dps,  lock):    
#        root=Toplevel(rt)
        
        root.title("DPS memory setup")
        
        self.root=root
        self.dps=dps

        self.lock=lock

        ENTRYWIDTH=10

        row=0
        col=0
        rowspan=1
        colspan=2
        self.ivarmem=IntVar()
        sc=Scale(root, label='Memory', variable=self.ivarmem, from_=0, to=9, resolution=1, orient="horizontal")
        sc.bind("<ButtonRelease-1>", self.sclcmdrecallmem)
        sc.grid(row=row, column=col, sticky=W+E, columnspan=colspan)
        col+=colspan
        Button(root, text="Active", command=self.butcmdactivemem).grid(row=row, column=col, columnspan=colspan, sticky=E+W, padx=8)
        col+=colspan
        Button(root, text='Store', command=self.butcmdstoremem).grid(row=row, column=col, columnspan=colspan, sticky=E+W, padx=8)

        colspan=1
        row+=rowspan
        col=0
        Label(root, text="Vset [V]: ", foreground=Scopetube.VCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvsetm=DoubleVar()
        Entry(root, textvariable=self.dvarvsetm, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Cset [A]: ", foreground=Scopetube.CCOL).grid(row=row, column=col, sticky=E)
        col+=1
        self.dvarcsetm=DoubleVar()
        Entry(root, textvariable=self.dvarcsetm, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        
        colspan=1
        row+=rowspan
        col=0
        Label(root, text="Vmax [V]: ", foreground=Scopetube.VCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvmax=DoubleVar()
        Entry(root, textvariable=self.dvarvmax, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Cmax [A]: ", foreground=Scopetube.CCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarcmax=DoubleVar()
        Entry(root, textvariable=self.dvarcmax, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Pmax [W]: ", foreground=Scopetube.PCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarpmax=DoubleVar()
        Entry(root, textvariable=self.dvarpmax, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)

        row+=rowspan
        colspan=1
        col=0
        Label(root, text="Brightness: ").grid(row=row, column=col, sticky=E)
        col+=colspan
        self.ivarbrght=IntVar()
        Entry(root, textvariable=self.ivarbrght, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)        
        col+=colspan
        colspan=2
        self.ivaroutmset=IntVar()
        self.ivaroutmset.set(0)
        Checkbutton(root, variable=self.ivaroutmset, text="Out@MSet", command=self.toimplement).grid(row=row, column=col, sticky=E+W, columnspan=colspan)
        col+=colspan
        self.ivaroutpwron=IntVar()
        self.ivaroutpwron.set(0)
        Checkbutton(root, variable=self.ivaroutpwron, text="Out@PwOn", command=self.toimplement).grid(row=row, column=col, sticky=E+W, columnspan=colspan)

        row+=rowspan
        colspan=2
        col=4
        Button(root, text="Done", command=self.btncmddone).grid(row=row, column=col, sticky=E+W, columnspan=colspan)
        
    def getmem(self):
        m=self.ivarmem.get()
        if m<0 or m>9:
            tkMessageBox.error('Memory location not available', 'Memory location goes from 0 to 9')
            raise ValueError('Memory location not available')        
        return m

    def memregs(self):
        mem='m'+str(self.getmem())
        return [mem+a for a in ['vset', 'cset',  'ovp', 'ocp', 'opp', 'bled', 'pre', 'onoff']]

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
            self.sclcmdrecallmem()

    def focus_set(self):
        self.root.focus_set()
        
    def toimplement(self):
        pass

    def btncmddone(self):
        self.root.destroy()
