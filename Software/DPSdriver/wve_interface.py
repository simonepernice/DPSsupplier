from Tkinter import Label, Button, Entry, StringVar, IntVar, DoubleVar, E, W,  Tk
from ttk import Separator

class Wveinterface:        
    ENTRYWIDTH=10

    def __init__(self, root,  dps):    
        root.title("DPS wave editor")
        
        self.root=root
        self.dps=dps

        row=0
        col=0
        rowspan=1
        colspan=1
        self.insertlabelrow(root, row, ('step', 'time [s]', 'pause [s]', 'voltage [V]', 'current [A]'))
#        Label(root, text='step').grid(row=row, column=col, columnspan=colspan)
#        col+=colspan
#        Label(root, text='time [s]').grid(row=row, column=col, columnspan=colspan)
#        col+=colspan
#        Label(root, text='pause [s]').grid(row=row, column=col, columnspan=colspan)
#        col+=colspan
#        Label(root, text='voltage [V]').grid(row=row, column=col, columnspan=colspan)
#        col+=colspan
#        Label(root, text='current [A]').grid(row=row, column=col, columnspan=colspan)
#        col+=colspan
        
        TABLEROW=8
        TABLECOL=5
        row+=rowspan
        col=0
        self.svararoutput=[]
        for r in range(TABLEROW):
            line=[]
            for c in range(TABLECOL):
                s=StringVar()
                s.set('r='+str(r)+'c='+str(c))
                line.append(s)
#                Entry(root, textvariable=s, width=Wveinterface.ENTRYWIDTH, state='readonly').grid(row=row+r, column=c)
                Label(root, textvariable=s, width=Wveinterface.ENTRYWIDTH, relief='ridge', justify='right').grid(row=row+r, column=c)
            self.svararoutput.append(line)

        row=1
        rowspan=1
        col=TABLECOL
        Button(root, text="Line up", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)
        col+=colspan        
        Button(root, text="Pick tme/stp", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)
        col=TABLECOL
        row+=rowspan
        Button(root, text="Page up", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)
        row+=rowspan
        Button(root, text="Top", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)        
        row+=rowspan
        Button(root, text="Goto Time", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)        
        col+=colspan
        self.ivargototime=IntVar()
        Entry(root, textvariable=self.ivargototime, width=Wveinterface.ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)
        row+=rowspan
        col=TABLECOL
        Button(root, text="Goto Step", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)        
        col+=colspan
        self.ivargotostep=IntVar()
        Entry(root, textvariable=self.ivargotostep, width=Wveinterface.ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)
        row+=rowspan
        col=TABLECOL
        Button(root, text="Bottom", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)
        row+=rowspan
        Button(root, text="Page down", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)
        row+=rowspan
        Button(root, text="Line down", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)      
        col+=colspan        
        Button(root, text="Pick tme/stp", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)        

        row+=rowspan
        col=0
        colspan=TABLECOL+2
        Separator(root, orient='horizontal').grid(row=row, columnspan=colspan, sticky=E+W, pady=8)

        row+=rowspan
        colspan=1
        self.insertlabelrow(root, row, ('step', 'time [s]', 'pause [s]', 'voltage [V]', 'current [A]')) 

        row+=rowspan
        self.ivarstep=IntVar()
        self.ivartime=IntVar()
        self.ivarpause=IntVar()
        self.dvarvoltage=DoubleVar()
        self.dvarcurrent=DoubleVar()
        self.insertentryrow(root, row, (self.ivarstep, self.ivartime, self.ivarpause, self.dvarvoltage, self.dvarcurrent)) 
        col=TABLECOL
        Button(root, text="Insert", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)
        col+=colspan
        Button(root, text="Modify", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)

        row+=rowspan
        col=0
        colspan=TABLECOL+2
        Separator(root, orient='horizontal').grid(row=row, columnspan=colspan, sticky=E+W, pady=8)

        row+=rowspan
        col=0
        colspan=1
        self.insertlabelrow(root, row, ('step beg.', 'time beg.[s]')) 
        
        row+=rowspan
        self.ivarstepbeg=IntVar()
        self.ivartimebeg=IntVar()
        self.insertentryrow(root, row, (self.ivarstepbeg, self.ivartimebeg))
        col=TABLECOL
        Button(root, text="Copy", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)
        col+=colspan
        Button(root, text="Cut", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)

        row+=rowspan
        col=0
        self.insertlabelrow(root, row, ('step end', 'time end[s]', 'paste times', 'ramp steps')) 
        
        row+=rowspan
        self.ivarstepend=IntVar()
        self.ivartimeend=IntVar()
        self.ivarpastetimes=IntVar()
        self.ivarrampsteps=IntVar()
        self.insertentryrow(root, row, (self.ivarstepend, self.ivartimeend, self.ivarpastetimes, self.ivarrampsteps))
        col=TABLECOL
        Button(root, text="Paste", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)
        col+=colspan
        Button(root, text="Ramp", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)

        row+=rowspan
        col=0
        colspan=TABLECOL+2
        Separator(root, orient='horizontal').grid(row=row, columnspan=colspan, sticky=E+W, pady=8)

        col=TABLECOL+1
        colspan=1
        row+=rowspan
        Button(root, text="Done", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)
#        
#        col+=colspan
#        Button(root, text='Store', command=self.butcmdstore).grid(row=row, column=col, columnspan=colspan, sticky=E+W, padx=8)
#
#        colspan=2
#        row+=rowspan
#        col=0
#        self.ivarmem=IntVar()
#        sc=Scale(root, variable=self.ivarmem, from_=0, to=9, resolution=1, orient="horizontal")#label='Memory', 
#        sc.grid(row=row, column=col, sticky=W+E, columnspan=colspan)
#        col+=colspan
#        colspan=4
#        Button(root, text='Active', command=self.butcmdactive).grid(row=row, column=col, columnspan=colspan, sticky=E+W, padx=8)        
#
#        colspan=1
#        row+=rowspan        
#        col=0
#        Label(root, text="Vset [V]: ", foreground=Scopetube.VCOL).grid(row=row, column=col, sticky=E)
#        col+=colspan
#        self.dvarvset=DoubleVar()
#        Entry(root, textvariable=self.dvarvset, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
#        col+=colspan
#        Label(root, text="Cset [A]: ", foreground=Scopetube.CCOL).grid(row=row, column=col, sticky=E)
#        col+=colspan
#        self.dvarcset=DoubleVar()
#        Entry(root, textvariable=self.dvarcset, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
#
#        colspan=1
#        row+=rowspan
#        col=0
#        Label(root, text="Vmax [V]: ", foreground=Scopetube.VCOL).grid(row=row, column=col, sticky=E)
#        col+=colspan
#        self.dvarvmax=DoubleVar()
#        Entry(root, textvariable=self.dvarvmax, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
#        col+=colspan
#        Label(root, text="Cmax [A]: ", foreground=Scopetube.CCOL).grid(row=row, column=col, sticky=E)
#        col+=colspan
#        self.dvarcmax=DoubleVar()
#        Entry(root, textvariable=self.dvarcmax, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
#        col+=colspan
#        Label(root, text="Pmax [W]: ", foreground=Scopetube.PCOL).grid(row=row, column=col, sticky=E)
#        col+=colspan
#        self.dvarpmax=DoubleVar()
#        Entry(root, textvariable=self.dvarpmax, width=ENTRYWIDTH).grid(row=row, column=col, sticky=W)
#
#        row+=rowspan
#        colspan=1
#        col=0
#        Label(root, text='Bright:').grid(row=row, column=col, columnspan=colspan)
#        col+=colspan      
#        self.ivarbrght=IntVar()
#        Scale(root, variable=self.ivarbrght, from_=0, to=5, resolution=1, orient="horizontal").grid(row=row, column=col, columnspan=colspan)#, label='Brightness'
#        col+=colspan
#        colspan=2
#        self.ivaroutmset=IntVar()
#        self.ivaroutmset.set(0)
#        Checkbutton(root, variable=self.ivaroutmset, text="Out same/off@MSet", command=self.toimplement).grid(row=row, column=col, sticky=E+W, columnspan=colspan)
#        col+=colspan
#        self.ivaroutpwron=IntVar()
#        self.ivaroutpwron.set(0)
#        Checkbutton(root, variable=self.ivaroutpwron, text="Out on/off@PwOn", command=self.toimplement).grid(row=row, column=col, sticky=E+W, columnspan=colspan)
#
#        row+=rowspan
#        colspan=2
#        col=4
#        Button(root, text="Done", command=self.btncmddone).grid(row=row, column=col, sticky=E+W, columnspan=colspan)


    def insertlabelrow(self, root, row, names):
        r=row
        c=0
        for n in names:
            Label(root, text=n).grid(row=r, column=c)
            c+=1
        return c


    def insertentryrow(self, root, row, vars):
        r=row
        c=0
        for v in vars:
            Entry(root, textvariable=v, width=Wveinterface.ENTRYWIDTH, justify='right').grid(row=r, column=c)
            c+=1
        return c

    def memregs(self):
        mem='m'+str(self.ivarmem.get())
        return [mem+a for a in ['vset', 'cset',  'ovp', 'ocp', 'opp', 'brght', 'pre', 'onoff']]

    def butcmdrecall(self):
        mr=self.memregs()
        self.lock.acquire()
        data=self.dps.get(mr)
        self.lock.release()
        self.dvarvset(data[0])
        self.dvarcset(data[1])
        self.dvarvmax.set(data[2])
        self.dvarcmax.set(data[3])
        self.dvarpmax.set(data[4])
        self.ivarbrght.set(data[5])
        self.ivaroutmset.set(data[6])
        self.ivaroutenab.set(data[7])
    
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
            self.ivaroutenab.get()
        ]
        self.lock.acquire()
        self.dps.set(mr, mv)
        self.lock.release()
 
    def butcmdactive(self):
        self.butcmdrecall()
        self.lock.acquire()
        self.dps.set(['mset'], [self.ivarmem.get()])
        self.lock.release()
        self.upfields()
        
    def toimplement(self):
        pass

    def btncmddone(self):
        self.root.destroy()

if __name__=='__main__':
    root=Tk()
    my_gui=Wveinterface(root,  None)
    root.mainloop()
