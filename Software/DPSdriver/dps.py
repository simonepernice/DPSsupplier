from dps_interface import DPSinterface
from Tkinter import Tk, PhotoImage

root=Tk()

root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='./pwrsup.png'))#'png'))

my_gui=DPSinterface(root)
root.mainloop()
