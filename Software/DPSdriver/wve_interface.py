from Tkinter import Label, Button, Entry, IntVar, DoubleVar, E, W
from ttk import Separator

from constants import ENTRYWIDTH, TABLEROW, TABLECOL
from table import Table

class Wveinterface:        

    def __init__(self, root,  fwave):    
        root.title("DPS wave editor")
        
        self.root=root
        self.fwave=fwave

        row=0
        col=0
        rowspan=1
        colspan=1
        self.insertlabelrow(root, row, ('step', 'time [s]', 'pause [s]', 'voltage [V]', 'current [A]'))

        row+=rowspan
        col=0

        self.viewrow=0
        self.wvedata=self.fwave.getpoints()
        self.table=Table(root, self.wvedata, row, col, TABLEROW, TABLECOL)
        
        row=1
        rowspan=1
        col=TABLECOL
        Button(root, text="Line up", command=self.butcmdlneup).grid(row=row, column=col, sticky=E+W, padx=8)
        col+=colspan        
        Button(root, text="Pick tme/stp", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)
        col=TABLECOL
        row+=rowspan
        Button(root, text="Page up", command=self.butcmdpgeup).grid(row=row, column=col, sticky=E+W, padx=8)
        row+=rowspan
        Button(root, text="Top", command=self.butcmdtop).grid(row=row, column=col, sticky=E+W, padx=8)        
        row+=rowspan
        Button(root, text="Goto Time", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)        
        col+=colspan
        self.ivargototime=IntVar()
        Entry(root, textvariable=self.ivargototime, width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)
        row+=rowspan
        col=TABLECOL
        Button(root, text="Goto Step", command=self.toimplement).grid(row=row, column=col, sticky=E+W, padx=8)        
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
        Button(root, text="Done", command=self.btncmddone).grid(row=row, column=col, sticky=E+W, padx=8)

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
            Entry(root, textvariable=v, width=ENTRYWIDTH, justify='right').grid(row=r, column=c)
            c+=1
        return c
        
    def toimplement(self):
        pass
    
    def butcmdlneup(self):
        self.viewrow-=1
        self.updateview()

    def butcmdpgeup(self):
        self.viewrow-=TABLEROW
        self.updateview()

    def butcmdtop(self):
        self.viewrow=0
        self.updateview()

    def butcmdlnedwn(self):
        self.viewrow+=1
        self.updateview()

    def butcmdpgedwn(self):
        self.viewrow+=TABLEROW
        self.updateview()

    def butcmdbottom(self):
        self.viewrow=len(self.wvedata)-1
        self.updateview()

    def updateview(self):
        if self.viewrow<0:
            self.viewrow=0
        elif self.viewrow>=len(self.wvedata):
            self.viewrow=len(self.wvedata)-1
        self.table.updateview(self.viewrow)
        

    def btncmddone(self):
        self.root.destroy()

if __name__=='__main__':
    from Tkinter import Tk
    from dpsfile import Dpsfile
    root=Tk()
    my_gui=Wveinterface(root,  Dpsfile())
    root.mainloop()
