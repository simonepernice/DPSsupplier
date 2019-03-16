from Tkinter import Label, DoubleVar

from constants import ENTRYWIDTH

class Table:
    
    def __init__(self, root,  data,  row0,  col0, tablerows, tablecols):    
        self.root=root
        self.data=data
        self.rows=tablerows
        
        self.dvararoutput=[]
        for r in range(tablerows):
            line=[]
            for c in range(tablecols):
                s=DoubleVar()
                line.append(s)
                Label(root, textvariable=s, width=ENTRYWIDTH, relief='ridge', justify='right').grid(row=row0+r, column=col0+c)
            self.dvararoutput.append(line)
            
        self.updateview(0)
            
    def updateview(self, row):
        rows=0
        for orow, drow in zip(self.dvararoutput, self.data[row:row+self.rows]):
            orow[0].set(row)
            row+=1
            rows+=1
            for ocol, dcol in zip(orow[1:], drow):
                ocol.set(round(dcol, 2))

        while rows<self.rows:#clean next fields not written if eny
            for ocol in self.dvararoutput[rows]:
                ocol.set(0)
            rows+=1

if __name__=='__main__':
    from Tkinter import Tk
    root=Tk()
    data=[]
    table=Table(root, data, 0, 0, 4, 4)
    data.append([3, 4, 5, 6])
    data.append([4, 5, 6, 3])
    data.append([5, 6, 3, 4])
    data.append([6, 3, 4, 5])
    table.updateview(1)
    root.mainloop()
