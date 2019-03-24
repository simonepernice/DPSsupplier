from Tkinter import Label, Button, Checkbutton, Entry, Scale, IntVar, DoubleVar, E, W

from constants import ENTRYWIDTH, VCOL, CCOL, PCOL

class Meminterface:        
    def __init__(self, root,  dps,  lock):    
        root.title("DPS memory setup")
        
        self.root=root
        self.dps=dps
        self.lock=lock

        row=0
        col=0
        colspan=2
        rowspan=1
        self.ivarmem=IntVar()
        Scale(root, label='Memory', variable=self.ivarmem, from_=0, to=9, resolution=1, orient="horizontal").grid(row=row, column=col, sticky=W+E, columnspan=colspan)
        col+=colspan
        Button(root, text="Recall", command=self.butcmdrecall).grid(row=row, column=col, columnspan=colspan, sticky=E+W, padx=8)
        col+=colspan
        Button(root, text='Store', command=self.butcmdstore).grid(row=row, column=col, columnspan=colspan, sticky=E+W, padx=8)     

        colspan=1
        row+=rowspan        
        col=0
        Label(root, text="Vset [V]: ", foreground=VCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvset=DoubleVar()
        Entry(root, textvariable=self.dvarvset, width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Cset [A]: ", foreground=CCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarcset=DoubleVar()
        Entry(root, textvariable=self.dvarcset, width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)

        colspan=1
        row+=rowspan
        col=0
        Label(root, text="Vmax [V]: ", foreground=VCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarvmax=DoubleVar()
        Entry(root, textvariable=self.dvarvmax, width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Cmax [A]: ", foreground=CCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarcmax=DoubleVar()
        Entry(root, textvariable=self.dvarcmax, width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)
        col+=colspan
        Label(root, text="Pmax [W]: ", foreground=PCOL).grid(row=row, column=col, sticky=E)
        col+=colspan
        self.dvarpmax=DoubleVar()
        Entry(root, textvariable=self.dvarpmax, width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)

        row+=rowspan
        colspan=1
        col=0
        Label(root, text='Bright:').grid(row=row, column=col, columnspan=colspan)
        col+=colspan      
        self.ivarbrght=IntVar()
        Scale(root, variable=self.ivarbrght, from_=0, to=5, resolution=1, orient="horizontal").grid(row=row, column=col, columnspan=colspan)#, label='Brightness'
        col+=colspan
        colspan=2
        self.ivaroutmset=IntVar()
        self.ivaroutmset.set(0)
        Checkbutton(root, variable=self.ivaroutmset, text="Out same/off@MSet", command=self.toimplement).grid(row=row, column=col, sticky=E+W, columnspan=colspan)
        col+=colspan
        self.ivaroutpwron=IntVar()
        self.ivaroutpwron.set(0)
        Checkbutton(root, variable=self.ivaroutpwron, text="Out on/off@PwOn", command=self.toimplement).grid(row=row, column=col, sticky=E+W, columnspan=colspan)

        row+=rowspan
        colspan=2
        col=4
        Button(root, text="Done", command=self.btncmddone).grid(row=row, column=col, sticky=E+W, columnspan=colspan)
        
        #self.butcmdrecall()

    def memregs(self):
        mem='m'+str(self.ivarmem.get())
        return [mem+a for a in ['vset', 'cset',  'ovp', 'ocp', 'opp', 'brght', 'pre', 'onoff']]

    def butcmdrecall(self):
        mr=self.memregs()
        self.lock.acquire()
        data=self.dps.get(mr)
        self.lock.release()
        self.dvarvset.set(data[0])
        self.dvarcset.set(data[1])
        self.dvarvmax.set(data[2])
        self.dvarcmax.set(data[3])
        self.dvarpmax.set(data[4])
        self.ivarbrght.set(data[5])
        self.ivaroutmset.set(data[6])
        self.ivaroutpwron.set(data[7])
    
    def butcmdstore(self):
        mr=self.memregs()
        mv=[
            self.dvarvset.get(), 
            self.dvarcset.get(), 
            self.dvarvmax.get(), 
            self.dvarcmax.get(), 
            self.dvarpmax.get(), 
            self.ivarbrght.get(), 
            self.ivaroutmset.get(), 
            self.ivaroutpwron.get()
        ]
        self.lock.acquire()
        self.dps.set(mr, mv)
        self.lock.release()
        
    def toimplement(self):
        pass

    def btncmddone(self):
        self.root.destroy()

if __name__=='__main__':
    from Tkinter import Tk
    root=Tk()
    my_gui=Meminterface(root,  None,  None)
    root.mainloop()
