from dps_interface import DPSinterface
from Tkinter import Tk, PhotoImage

if __name__=='__main__':
    root=Tk()

    root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='pwrsup.png'))

    my_gui=DPSinterface(root)
    root.mainloop()
