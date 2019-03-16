from Tkinter import Label, Button, Entry, IntVar, DoubleVar, E, W
from ttk import Separator

from constants import ENTRYWIDTH, TABLEROW, TABLECOL, CLIPROW, VCOL, CCOL, BCOL
from table import Table

class Wveinterface:        

    def __init__(self, root, fwave):    
        root.title("DPS wave editor")
        
        self.root=root
        self.fwave=fwave

        self.clipboard=[]
        self.clipboardtime=0

        row=0
        col=0
        rowspan=1
        colspan=1
        self.insertlabelrow(root, row, (('step', BCOL), ('time [s]', BCOL), ('voltage [V]', VCOL), ('current [A]', CCOL)))

        row+=rowspan
        col=0
        self.viewrowwve=0
        self.datawve=self.fwave.getpoints()
        self.tablewve=Table(root, self.datawve, row, col, TABLEROW, TABLECOL)
        
        row=1
        rowspan=1
        col=TABLECOL
        Button(root, text="Line up", command=self.butcmdlneup).grid(row=row, column=col, sticky=E+W, padx=8)
        col+=colspan        
        Button(root, text="Pick beg", command=self.btncmdpckbeg).grid(row=row, column=col, sticky=E+W, padx=8)
        col=TABLECOL
        row+=rowspan
        Button(root, text="Page up", command=self.butcmdpgeup).grid(row=row, column=col, sticky=E+W, padx=8)
        col+=colspan        
        Button(root, text="Pick end", command=self.btncmdpckend).grid(row=row, column=col, sticky=E+W, padx=8)
        col=TABLECOL
        row+=rowspan
        Button(root, text="Top", command=self.butcmdtop).grid(row=row, column=col, sticky=E+W, padx=8)        
        row+=rowspan
        Button(root, text="Goto Time", command=self.butcmdgototime).grid(row=row, column=col, sticky=E+W, padx=8)        
        col+=colspan
        self.dvargototime=DoubleVar()
        Entry(root, textvariable=self.dvargototime, width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)
        row+=rowspan
        col=TABLECOL
        Button(root, text="Goto Step", command=self.butcmdgotostep).grid(row=row, column=col, sticky=E+W, padx=8)        
        col+=colspan
        self.ivargotostep=IntVar()
        Entry(root, textvariable=self.ivargotostep, width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)
        row+=rowspan
        col=TABLECOL
        Button(root, text="Bottom", command=self.butcmdbottom).grid(row=row, column=col, sticky=E+W, padx=8)
        row+=rowspan
        Button(root, text="Page down", command=self.butcmdpgedwn).grid(row=row, column=col, sticky=E+W, padx=8)
        row+=rowspan
        Button(root, text="Line down", command=self.butcmdlnedwn).grid(row=row, column=col, sticky=E+W, padx=8)      

        row+=rowspan
        col=0
        colspan=TABLECOL+2
        Separator(root, orient='horizontal').grid(row=row, columnspan=colspan, sticky=E+W, pady=8)

        row+=CLIPROW
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
        self.insertlabelrow(root, row, (('step', BCOL), ('dt [s]', BCOL), ('voltage [V]', VCOL), ('current [A]', CCOL)))

        row+=rowspan
        col=0
        self.viewrowclp=0
        self.tableclipboard=Table(root, self.clipboard, row, col, CLIPROW, TABLECOL)
        
        col=TABLECOL
        Button(root, text="Line up", command=self.butcmdlneupcp).grid(row=row, column=col, sticky=E+W, padx=8)
        row+=rowspan
        Button(root, text="Page up", command=self.butcmdpgeupcp).grid(row=row, column=col, sticky=E+W, padx=8)
        row+=rowspan
        Button(root, text="Page down", command=self.butcmdpgedwncp).grid(row=row, column=col, sticky=E+W, padx=8)
        row+=rowspan
        Button(root, text="Line down", command=self.butcmdlnedwncp).grid(row=row, column=col, sticky=E+W, padx=8)               

        row+=rowspan
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
        Button(root, text="Ramp Clipb", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)
#        col+=colspan
#        Button(root, text="Trans Clipb", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)

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
        self.updateview()

    def butcmddelete(self):
        del self.datawve[self.ivarstep.get()]
        self.updateview()

    def butcmdinsert(self):
        self.datawve.insert(self.findtime(self.dvartime.get()),[self.dvartime.get(), self.dvarvoltage.get(), self.dvarcurrent.get()])
        self.updateview()

    def butcmdappend(self):
        self.datawve.append([self.dvarpause.get()+self.datawve[-1][0], self.dvarvoltage.get(), self.dvarcurrent.get()])
        self.updateview()
    
    def butcmdgototime(self):
        self.viewrowwve=self.findtime(self.dvargototime.get())-1
        self.updateview()

    def butcmdgotostep(self):
        self.viewrowwve=self.ivargotostep.get()
        self.updateview()

    def butcmdlneupcp(self):
        self.viewrowclp-=1
        self.updateviewclp()

    def butcmdpgeupcp(self):
        self.viewrowclp-=(CLIPROW-1)
        self.updateviewclp()

    def butcmdlneup(self):
        self.viewrowwve-=1
        self.updateview()

    def butcmdpgeup(self):
        self.viewrowwve-=(TABLEROW-1)
        self.updateview()

    def butcmdtop(self):
        self.viewrowwve=0
        self.updateview()

    def butcmdlnedwncp(self):
        self.viewrowclp+=1
        self.updateviewclp()

    def butcmdpgedwncp(self):
        self.viewrowclp+=(CLIPROW-1)
        self.updateviewclp()

    def butcmdlnedwn(self):
        self.viewrowwve+=1
        self.updateview()

    def butcmdpgedwn(self):
        self.viewrowwve+=(TABLEROW-1)
        self.updateview()

    def butcmdbottom(self):
        self.viewrowwve=len(self.datawve)-1
        self.updateview()
        
    def btncmdpckbeg(self):
        r=self.viewrowwve
        self.ivarstep.set(r)
        self.dvartime.set(self.datawve[r][0])
        self.dvarvoltage.set(self.datawve[r][1])
        self.dvarcurrent.set(self.datawve[r][2])

        self.ivarstepbeg.set(r)

        self.ivarstepend.set(r)

    def btncmdpckend(self):
        r=self.viewrowwve+1
        self.ivarstep.set(r)
        self.dvartime.set(self.datawve[r][0])
        self.dvarvoltage.set(self.datawve[r][1])
        self.dvarcurrent.set(self.datawve[r][2])

        self.ivarstepend.set(r)

    def butcmdcopy(self):
        del self.clipboard[:]
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
            self.clipboard.append([t1-t0]+lne[1:])
            t0=t1
        
        self.clipboardtime=t0-t00
        self.tableclipboard.updateview(self.viewrowclp)

    def butcmdcut(self):
        self.butcmdcopy()
        
        sb=self.ivarstepbeg.get()
        for i in range(self.ivarstepend.get()-sb+1):
            del self.datawve[sb]
            
        for i in range(self.ivarstepend.get()-sb+1, len(self.datawve)):
            self.datawve[i][0]-=self.clipboardtime

        self.updateview()

    def paste(self):
        i=self.ivarpastestep.get()
        if i>0:
            t0=self.datawve[i-1][0]
        else:
            t0=0

        for t in range(self.ivarpastetimes.get()):
            for lne in self.clipboard:
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

        self.updateview()

    def butcmdpasteovw(self):
        i=self.paste()
        
        if i>0:
            t0=self.datawve[i-1][0]
        else:
            t0=0

        while i<len(self.datawve) and self.datawve[i][0]<=t0:
            del self.datawve[i]

        self.updateview()

    def butcmdampliclip(self):
        coeff=(self.dvartcoeff.get(), self.dvarvcoeff.get(), self.dvarccoeff.get())
        acc=0
        for l in self.clipboard:
            for i in range(3):
                l[i]*=coeff[i]
            acc+=l[0]
        self.clipboardtime=acc
        
        self.tableclipboard.updateview(self.viewrowclp)

    def butcmdtransclip(self):
        coeff=(self.dvartcoeff.get(), self.dvarvcoeff.get(), self.dvarccoeff.get())
        acc=0
        for l in self.clipboard:
            for i in range(3):
                l[i]+=coeff[i]
            acc+=l[0]
        self.clipboardtime=acc
        
        self.tableclipboard.updateview(self.viewrowclp)
        
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
        
    def toimplement(self):
        pass

    def findtime(self, t):
        for r in range(len(self.datawve)):
            if self.datawve[r][0]>t :
                break
        return r

    def updateviewclp(self):
        if self.viewrowclp<0:
            self.viewrowclp=0
        elif self.viewrowclp>=len(self.clipboard):
            self.viewrowclp=len(self.clipboard)-1 
        
        self.tableclipboard.updateview(self.viewrowclp) 
    
    def updateview(self):
        if self.viewrowwve<0:
            self.viewrowwve=0
        elif self.viewrowwve>=len(self.datawve):
            self.viewrowwve=len(self.datawve)-1        
        
        self.tablewve.updateview(self.viewrowwve)        

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
