from Tkinter import Text, END, DISABLED
from toplevel import maketoplevel

class Txtinterface:        
    def __init__(self, prevroot,  title,  txt,  readfromfile=False, width=40, height=20):        
        self.root=maketoplevel(prevroot, True)
        self.root.title(title)
        
        outputtext=Text(self.root, width=width, height=height)
        
        if readfromfile:
            with open(txt) as infile:
                outputtext.insert(END, infile.read())
        else:
             outputtext.insert(END, txt)
        outputtext.config(state=DISABLED)
        
        outputtext.pack()
                    

if __name__=='__main__':
    from Tkinter import Tk
    root=Tk()
    my_gui=Txtinterface(root,  'info',  'This is just\Several lines of \ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext')
    root.mainloop()
