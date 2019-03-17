from Tkinter import Label, Button, Entry, IntVar, DoubleVar, E, W
from ttk import Separator

from constants import ENTRYWIDTH, TABLEROW, TABLECOL, CLIPROW, VCOL, CCOL, BCOL
from table import Table

class Wveinterface:        

    def __init__(self, root, fwave):    
        root.title("DPS wave editor")
        
        self.root=root
        self.fwave=fwave
        self.datawve=self.fwave.getpoints()

        self.dataclpbrd=[]
        self.clipboardtime=0

        row=0
        col=0        
        self.tablewve=Table(root, self.datawve, (('step', BCOL), ('time [s]', BCOL), ('voltage [V]', VCOL), ('current [A]', CCOL)), row, col, TABLEROW, TABLECOL)
        
        row=1
        rowspan=1
        colspan=1
        col=TABLECOL+colspan
        Button(root, text="Pick beg", command=self.btncmdpckbeg).grid(row=row, column=col, sticky=E+W, padx=8)
        col=TABLECOL+colspan        
        row+=rowspan
        Button(root, text="Pick end", command=self.btncmdpckend).grid(row=row, column=col, sticky=E+W, padx=8)

        row=TABLEROW+1
        col=0
        colspan=TABLECOL+2
        Separator(root, orient='horizontal').grid(row=row, columnspan=colspan, sticky=E+W, pady=8)

        row+=rowspan
        colspan=1
        self.insertlabelrow(root, row, (None, None, ('voltage [V]', VCOL), ('current [A]', CCOL))) 

        row+=rowspan
        self.insertlabelrow(root, row, ( ('time [s]:', BCOL), ))
        self.dvartime=DoubleVar()
        self.dvarvoltage=DoubleVar()
        self.dvarcurrent=DoubleVar()
        self.insertentryrow(root, row, (None, self.dvartime, self.dvarvoltage, self.dvarcurrent)) 
        col=TABLECOL
        Button(root, text="Insert", command=self.butcmdinsert).grid(row=row, column=col, sticky=E+W, padx=8)

        row+=rowspan
        self.insertlabelrow(root, row, ( ('step :', BCOL), ))        
        self.ivarstep=IntVar()
        self.insertentryrow(root, row, (None, self.ivarstep, self.dvarvoltage, self.dvarcurrent)) 
        col=TABLECOL
        Button(root, text="Modify", command=self.butcmdmodify).grid(row=row, column=col, sticky=E+W, padx=8)
        col+=colspan
        Button(root, text="Delete", command=self.butcmddelete).grid(row=row, column=col, sticky=E+W, padx=8)

        row+=rowspan
        self.insertlabelrow(root, row, ( ('pause [s]:', BCOL), ))        
        self.dvarpause=DoubleVar()
        self.insertentryrow(root, row, (None, self.dvarpause, self.dvarvoltage, self.dvarcurrent)) 
        col=TABLECOL
        Button(root, text="Append", command=self.butcmdappend).grid(row=row, column=col, sticky=E+W, padx=8)

        row+=rowspan
        col=0
        colspan=TABLECOL+2
        Separator(root, orient='horizontal').grid(row=row, columnspan=colspan, sticky=E+W, pady=8)

        row+=rowspan
        col=0
        self.tableclipboard=Table(root, self.dataclpbrd,  (('step', BCOL), ('dt [s]', BCOL), ('voltage [V]', VCOL), ('current [A]', CCOL)), row, col, CLIPROW, TABLECOL) 

        row+=CLIPROW+1
        col=0
        colspan=1
        self.insertlabelrow(root, row, (('beg step', BCOL), None, ('end step', BCOL)))        
        self.ivarstepbeg=IntVar()
        self.ivarstepend=IntVar()
        self.insertentryrow(root, row, (None, self.ivarstepbeg, None, self.ivarstepend))
        col=TABLECOL
        Button(root, text="Copy", command=self.butcmdcopy).grid(row=row, column=col, sticky=E+W, padx=8)
        col+=colspan
        Button(root, text="Cut", command=self.butcmdcut).grid(row=row, column=col, sticky=E+W, padx=8)

        row+=rowspan
        col=0
        self.insertlabelrow(root, row, (('paste step', BCOL), None, ('paste times', BCOL))) 
        self.ivarpastestep=IntVar()
        self.ivarpastetimes=IntVar()
        self.ivarpastetimes.set(1)
        self.insertentryrow(root, row, (None, self.ivarpastestep, None, self.ivarpastetimes))
        col=TABLECOL
        Button(root, text="Paste Insert", command=self.butcmdpasteins).grid(row=row, column=col, sticky=E+W, padx=8)
        col+=colspan
        Button(root, text="Paste Overwrt", command=self.butcmdpasteovw).grid(row=row, column=col, sticky=E+W, padx=8)
        
        row+=rowspan
        col=0
        self.insertlabelrow(root, row, ( ('t,v,c m|q', BCOL),)) 
        self.dvartcoeff=DoubleVar()
        self.dvarvcoeff=DoubleVar()
        self.dvarccoeff=DoubleVar()
        self.insertentryrow(root, row, (None, self.dvartcoeff, self.dvarvcoeff, self.dvarccoeff))
        col=TABLECOL
        Button(root, text="Ampli Clipb", command=self.butcmdampliclip).grid(row=row, column=col, sticky=E+W, padx=8)
        col+=colspan
        Button(root, text="Trans Clipb", command=self.butcmdtransclip).grid(row=row, column=col, sticky=E+W, padx=8)
        
        row+=rowspan
        col=0
        self.insertlabelrow(root, row, (('ramp steps', BCOL), )) 
        self.ivarrampsteps=IntVar()
        self.ivarrampsteps.set(10)
        self.insertentryrow(root, row, (None, self.ivarrampsteps))
        col=TABLECOL
        Button(root, text="Ramp Clipb", command=self.butcmdramp).grid(row=row, column=col, sticky=E+W, padx=8)

        row+=rowspan
        col=0
        colspan=TABLECOL+2
        Separator(root, orient='horizontal').grid(row=row, columnspan=colspan, sticky=E+W, pady=8)

        col=TABLECOL+1
        colspan=1
        row+=rowspan
        Button(root, text="Done", command=self.butcmddone).grid(row=row, column=col, sticky=E+W, padx=8)

    def butcmdmodify(self):
        self.datawve[self.ivarstep.get()]=[self.datawve[self.ivarstep.get()][0], self.dvarvoltage.get(), self.dvarcurrent.get()]
        self.tablewve.updateview()

    def butcmddelete(self):
        del self.datawve[self.ivarstep.get()]
        self.tablewve.updateview()

    def butcmdinsert(self):
        self.datawve.insert(self.findtime(self.dvartime.get()),[self.dvartime.get(), self.dvarvoltage.get(), self.dvarcurrent.get()])
        self.tablewve.updateview()

    def butcmdappend(self):
        self.datawve.append([self.dvarpause.get()+self.datawve[-1][0], self.dvarvoltage.get(), self.dvarcurrent.get()])
        self.tablewve.updateview()
        
    def btncmdpckbeg(self):
        r=self.tablewve.getfistvisiblerow()
        self.ivarstep.set(r)
        self.dvartime.set(self.datawve[r][0])
        self.dvarvoltage.set(self.datawve[r][1])
        self.dvarcurrent.set(self.datawve[r][2])

        self.ivarstepbeg.set(r)

        self.ivarstepend.set(r)

    def btncmdpckend(self):
        r=self.tablewve.getfistvisiblerow()+1
        self.ivarstep.set(r)
        self.dvartime.set(self.datawve[r][0])
        self.dvarvoltage.set(self.datawve[r][1])
        self.dvarcurrent.set(self.datawve[r][2])

        self.ivarstepend.set(r)

    def butcmdcopy(self):
        del self.dataclpbrd[:]
        self.clipboardtime=0
        
        sb=self.ivarstepbeg.get()
        if sb>0:
            t0=self.datawve[sb-1][0]
        else:
            t0=0
        t00=t0

        for i in range(sb, self.ivarstepend.get()+1):
            lne=self.datawve[i]
            t1=lne[0]
            self.dataclpbrd.append([t1-t0]+lne[1:])
            t0=t1
        
        self.clipboardtime=t0-t00
        self.tableclipboard.updateview()

    def butcmdcut(self):
        self.butcmdcopy()
        
        sb=self.ivarstepbeg.get()
        for i in range(self.ivarstepend.get()-sb+1):
            del self.datawve[sb]
            
        for i in range(self.ivarstepend.get()-sb+1, len(self.datawve)):
            self.datawve[i][0]-=self.clipboardtime

        self.tablewve.updateview()

    def paste(self):
        i=self.ivarpastestep.get()
        if i>0:
            t0=self.datawve[i-1][0]
        else:
            t0=0

        for t in range(self.ivarpastetimes.get()):
            for lne in self.dataclpbrd:
                t1=lne[0]+t0
                self.datawve.insert(i, [t1]+lne[1:])
                i+=1
                t0=t1
        
        return i
                
    def butcmdpasteins(self):
        i=self.paste()

        dt=self.clipboardtime*self.ivarpastetimes.get()
        for i in range(i, len(self.datawve)):
            self.datawve[i][0]+=dt

        self.tablewve.updateview()

    def butcmdpasteovw(self):
        i=self.paste()
        
        if i>0:
            t0=self.datawve[i-1][0]
        else:
            t0=0

        while i<len(self.datawve) and self.datawve[i][0]<=t0:
            del self.datawve[i]

        self.tablewve.updateview()

    def butcmdampliclip(self):
        coeff=(self.dvartcoeff.get(), self.dvarvcoeff.get(), self.dvarccoeff.get())
        acc=0
        for l in self.dataclpbrd:
            for i in range(3):
                l[i]*=coeff[i]
            acc+=l[0]
        self.clipboardtime=acc
        
        self.tableclipboard.updateview()

    def butcmdtransclip(self):
        coeff=(0, self.dvarvcoeff.get(), self.dvarccoeff.get()) #time is not traslated because stored as delta on the clipboard

        for l in self.dataclpbrd:
            for i in range(1, 3):
                l[i]+=coeff[i]

        self.dataclpbrd[0][0]+=self.dvartcoeff.get()
        self.clipboardtime+=self.dvartcoeff.get()
        
        self.tableclipboard.updateview()
        
    def butcmddone(self):
        self.root.destroy()
        
    def insertlabelrow(self, root, row, names):
        c=0
        for n in names:
            if n is not None:
                Label(root, text=n[0], foreground=n[1]).grid(row=row, column=c)
            c+=1
        return c

    def insertentryrow(self, root, row, vars):
        r=row
        c=0
        for v in vars:
            if v is not None:
                Entry(root, textvariable=v, width=ENTRYWIDTH, justify='right').grid(row=r, column=c)
            c+=1
        return c
        
    def butcmdramp(self):
        beg=self.dataclpbrd[0][1:]
        end=self.dataclpbrd[-1][1:]
        steps=self.ivarrampsteps.get()-1
        deltastep=[(e-b)/steps for e, b in zip(end, beg)]
        tstep=(self.clipboardtime-self.dataclpbrd[0][0])/steps
        del self.dataclpbrd[1:]
        for s in range( steps):
            beg=[a+b for a, b in zip(beg, deltastep)]
            self.dataclpbrd.append([tstep]+beg)
        self.tableclipboard.updateview()
        
    def toimplement(self):
        pass

if __name__=='__main__':
    from Tkinter import Tk
    from dpsfile import Dpsfile
    root=Tk()
    points=[]
    for r in range(1,35):
        line=[]
        for c in range(3):
            line.append(r*10+1.11*(c+1))
        points.append(line)
            
    my_gui=Wveinterface(root,  Dpsfile(points))
    root.mainloop()
