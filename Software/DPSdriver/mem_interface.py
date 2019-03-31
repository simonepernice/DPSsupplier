from Tkinter import Label, Button, Checkbutton, Scale, IntVar, DoubleVar, E, W

from constants import VCOL, CCOL, PCOL
from gridlayoutrowinsert import insertlabelrow, insertentryrow

class Meminterface:        
    def __init__(self, root,  dps, updatefields):                
        self.root=root
        self.root.title("Memory editor")
        
        self.dps=dps
        self.updatefields=updatefields

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
       
        insertlabelrow(root, row, col, (("Vset [V]: ", VCOL), None, ("Cset [A]: ", CCOL)), E)
        self.dvarvset=DoubleVar()
        self.dvarcset=DoubleVar()
        insertentryrow(root, row, col, (None, self.dvarvset, None, self.dvarcset), 'right', W)

        colspan=1
        row+=rowspan
        col=0

        insertlabelrow(root, row, col, (("Vmax [V]: ", VCOL), None, ("Cmax [A]: ", CCOL), None, ("Pmax [W]: ", PCOL)), E)
        self.dvarvmax=DoubleVar()
        self.dvarcmax=DoubleVar()
        self.dvarpmax=DoubleVar()
        insertentryrow(root, row, col, (None, self.dvarvmax, None, self.dvarcmax, None, self.dvarpmax), 'right', W)

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
        Checkbutton(root, variable=self.ivaroutmset, text="Out same/off@MSet").grid(row=row, column=col, sticky=E+W, columnspan=colspan)
        col+=colspan
        self.ivaroutpwron=IntVar()
        self.ivaroutpwron.set(0)
        Checkbutton(root, variable=self.ivaroutpwron, text="Out on/off@PwOn").grid(row=row, column=col, sticky=E+W, columnspan=colspan)

        row+=rowspan
        colspan=2
        col=4
        Button(root, text="Done", command=self.btncmddone).grid(row=row, column=col, sticky=E+W, columnspan=colspan)

    def memregs(self):
        mem='m'+str(self.ivarmem.get())
        return [mem+a for a in ['vset', 'cset',  'ovp', 'ocp', 'opp', 'brght', 'pre', 'onoff']]

    def butcmdrecall(self):
        mr=self.memregs()
        data=self.dps.get(mr)
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
        self.dps.set(mr, mv)
        if self.ivarmem.get()==0:
            self.updatefields(True)

    def btncmddone(self):
        self.root.destroy()

if __name__=='__main__':
    from Tkinter import Tk
    root=Tk()
    my_gui=Meminterface(root,  None,  None)
    root.mainloop()
