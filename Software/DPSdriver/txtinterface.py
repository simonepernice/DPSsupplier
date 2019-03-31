from Tkinter import Text, END, DISABLED

class Txtinterface:        
    def __init__(self, root,  title,  txt,  readfromfile=False, width=40, height=20):                
        self.root=root
        self.root.title(title)
        
        outputtext=Text(root, width=width, height=height)
        
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
