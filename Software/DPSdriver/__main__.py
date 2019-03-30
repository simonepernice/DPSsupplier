from dps_interface import DPSinterface
from Tkinter import Tk, PhotoImage

if __name__=='__main__':
    root=Tk()

    try:
        root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='pwrsup.png'))
    except:
        print ('It is not possible to load the application icon')

    my_gui=DPSinterface(root)
    root.mainloop()
