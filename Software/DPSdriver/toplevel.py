from Tkinter import Toplevel, PhotoImage, Tk

def maketoplevel(root, modal=False):
    tl=Toplevel(root)
    try:
        tl.tk.call('wm', 'iconphoto', tl._w, PhotoImage(file='pwrsup.png'))
    except:
        print ('It is not possible to load the application icon')

    if modal:
        tl.grab_set()
        tl.focus_force()
        
    return tl
    
def makeroot():
    root=Tk()
    try:
        root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='pwrsup.png'))
    except:
        print ('It is not possible to load the application icon')
        
    return root
