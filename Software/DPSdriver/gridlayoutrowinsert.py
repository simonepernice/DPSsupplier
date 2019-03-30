from Tkinter import Label, Entry, NORMAL

from constants import ENTRYWIDTH, BCOL


def insertlabelrow(root, row, col, names, sticky=''):
    labellist=[]
    for n in names:
        if n is not None:
            if isinstance(n, tuple):
                t=n[0]
                c=n[1]
            else:
                t=n
                c=BCOL
            l=Label(root, text=t, foreground=c)
            l.grid(row=row, column=col, sticky=sticky)
            labellist.append(l)
        col+=1
    return labellist

def insertentryrow(root, row, col, vars, justify='right', sticky='', state=NORMAL):
    entrylist=[]
    r=row
    for v in vars:
        if v is not None:                
            e=Entry(root, textvariable=v, width=ENTRYWIDTH, justify=justify, state=state)
            e.grid(row=r, column=col, sticky=sticky)
            entrylist.append(e)
        col+=1
    return entrylist
