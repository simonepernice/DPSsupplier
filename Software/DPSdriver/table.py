from constants import ENTRYWIDTH, TPOS
from gridlayoutrowinsert import insertlabelrow

try:
    from Tkinter import Label, DoubleVar, IntVar, Button, E, W, Entry
except ImportError:
    from tkinter import Label, DoubleVar, IntVar, Button, E, W, Entry


class Table:
    
    def __init__(self, root,  data,  labels, row0,  col0, NROWS, NCOLS):    
        self.root=root
        self.data=data
        self.NROWS=NROWS
        self.firstvisiblerow=0

        insertlabelrow(root, row0, col0, labels)
        
        self.dvararoutput=[]
        for r in range(NROWS):
            line=[]
            for c in range(NCOLS):
                s=DoubleVar()
                line.append(s)
                Label(root, textvariable=s, width=ENTRYWIDTH, relief='ridge', justify='right').grid(row=row0+r+1, column=col0+c)
            self.dvararoutput.append(line)
        
        colspan=1
        rowspan=1
        row=row0+1
        col=col0+NCOLS        
        if NROWS>=2:
            Button(root, text="Line up", command=self.butcmdlneup).grid(row=row, column=col, sticky=E+W, padx=8)
            row+=rowspan
            if NROWS>=4:
                Button(root, text="Page up", command=self.butcmdpgeup).grid(row=row, column=col, sticky=E+W, padx=8)
                row+=rowspan
                if NROWS>=6:
                    Button(root, text="Top", command=self.butcmdtop).grid(row=row, column=col, sticky=E+W, padx=8)        
                    row+=rowspan
                    if NROWS>=8:
                        Button(root, text="Goto Time", command=self.butcmdgototime).grid(row=row, column=col, sticky=E+W, padx=8)        
                        col+=colspan
                        self.dvargototime=DoubleVar()
                        Entry(root, textvariable=self.dvargototime, width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)
                        row=NROWS-3
                        col=col0+NCOLS
                        Button(root, text="Goto Step", command=self.butcmdgotostep).grid(row=row, column=col, sticky=E+W, padx=8)        
                        col+=colspan
                        self.ivargotostep=IntVar()
                        Entry(root, textvariable=self.ivargotostep, width=ENTRYWIDTH, justify='right').grid(row=row, column=col, sticky=W)
                        row+=rowspan
                    col=col0+NCOLS
                    Button(root, text="Bottom", command=self.butcmdbottom).grid(row=row, column=col, sticky=E+W, padx=8)
                    row+=rowspan
                Button(root, text="Page down", command=self.butcmdpgedwn).grid(row=row, column=col, sticky=E+W, padx=8)
                row+=rowspan
            Button(root, text="Line down", command=self.butcmdlnedwn).grid(row=row, column=col, sticky=E+W, padx=8)      
        
        self.updateview()
    
    def getfistvisiblerow(self):
        return self.firstvisiblerow

    def updateview(self):
        if self.firstvisiblerow<0:
            self.firstvisiblerow=0
        elif self.firstvisiblerow>=len(self.data):
            self.firstvisiblerow=len(self.data)-1        
    
        row=self.firstvisiblerow
        rows=0
        for orow, drow in zip(self.dvararoutput, self.data[row:row+self.NROWS]):
            orow[0].set(row)
            row+=1
            rows+=1
            for ocol, dcol in zip(orow[1:], drow):
                ocol.set(round(dcol, 2))

        while rows<self.NROWS:#clean next fields not written if eny
            for ocol in self.dvararoutput[rows]:
                ocol.set('')
            rows+=1

    def butcmdgototime(self):
        self.firstvisiblerow=self.findtime(self.dvargototime.get())-1
        self.updateview()

    def butcmdgotostep(self):
        self.firstvisiblerow=self.ivargotostep.get()
        self.updateview()

    def butcmdlneup(self):
        self.firstvisiblerow-=1
        self.updateview()

    def butcmdpgeup(self):
        self.firstvisiblerow-=(self.NROWS-1)
        self.updateview()

    def butcmdtop(self):
        self.firstvisiblerow=0
        self.updateview()

    def butcmdlnedwn(self):
        self.firstvisiblerow+=1
        self.updateview()

    def butcmdpgedwn(self):
        self.firstvisiblerow+=(self.NROWS-1)
        self.updateview()

    def butcmdbottom(self):
        self.firstvisiblerow=len(self.data)-1
        self.updateview()
    
    def findtime(self, t):
        for r in range(len(self.data)):
            if self.data[r][TPOS]>t :
                break
        else:
            r=len(self.data)
        return r

if __name__=='__main__':
    try:
        from Tkinter import Tk
    except ImportError:
        from tkinter import Tk

    root=Tk()
    data=[]
    table=Table(root, data,  (('step', 'black'), ('time [s]', 'black'), ('voltage [V]', 'red'), ('current [A]', 'blue')), 0, 0, 10, 4)
    for r in range(20):
        l=[]
        for c in range(1, 5):
            l.append(r*10+c)
        data.append(l)

    table.updateview()
    root.mainloop()
