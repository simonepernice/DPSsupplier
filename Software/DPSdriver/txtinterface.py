from toplevel import maketoplevel

try:
    from Tkinter import Text, END, DISABLED, Button, BOTH
except ImportError:
    from tkinter import Text, END, DISABLED, Button, BOTH

class Txtinterface:        
    def __init__(self, prevroot,  title,  txt,  readfromfile=False, width=-1, height=-1):        
        self.root=maketoplevel(prevroot, True)
        self.root.title(title)
        
        if width<0 or height<0:
            h=0
            w=0
            for line in txt.split('\n'):
                if len(line) > w: w = len(line)
                h+=1
            if width < 0: width = w
            if height < 0: height = h

        outputtext=Text(self.root, width=width, height=height)
        
        if readfromfile:
            with open(txt) as infile:
                outputtext.insert(END, infile.read())
        else:
             outputtext.insert(END, txt)
        outputtext.config(state=DISABLED)
        
        outputtext.pack(fill=BOTH, expand=1)
        
        Button(self.root, text="OK", command=self.butcmdok).pack()   
    
    def butcmdok(self):
        self.root.destroy()

if __name__=='__main__':
    try:
        from Tkinter import Tk
    except ImportError:
        from tkinter import Tk

    root=Tk()
    my_gui=Txtinterface(root,  'info',  'This is just\Several lines of \ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext')
    root.mainloop()
