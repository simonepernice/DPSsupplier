import os

try:
    from Tkinter import Toplevel, PhotoImage, Tk
except ImportError:
    from tkinter import Toplevel, PhotoImage, Tk

def maketoplevel(root, modal=False):
    tl=Toplevel(root)
    try:
        root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pwrsup.png')))
    except:
        print ('It is not possible to load the application icon')

    if modal:
        tl.grab_set()
        tl.focus_force()
        
    return tl
    
def makeroot():
    root=Tk()
    try:
        root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pwrsup.png')))
    except:
        print ('It is not possible to load the application icon')
        
    return root

def maindir():
    pass
