"""
 DPS interface: an interface for DPS supplier

 Clipboard class is used to make a clipboard to manage wave data.

 (C)2019 - Simone Pernice - pernice@libero.it
  This is distributed under GNU LGPL license, see license.txt

 (C)2009 - Luc Jean - luc.jean@gmail.com
 (C)2009 - Apidev - http://www.apidev.fr

"""

from Tkinter import Button, IntVar, DoubleVar, E, W

from constants import TABLECOL, CLIPROW, VCOL, CCOL, TPOS
from table import Table
from gridlayoutrowinsert import insertlabelrow, insertentryrow


class Clipboard:

    """
    Clipboard is a standard clipboar with copy, cut and past functions.

    It is showed as table that can be scrolled and several buttons to operate.
    Compared to a standard clipboard it has the function paste-overwrite.
    It has also the function ramp to transform two levels in a ramp.

    """

    def __init__(self, root, datawve, updateview, row0, col0):
        """
        Create a Clipboard.

        :param root is the top level Tkinterface where the clipboard sits.
        :datawve: is the list of poins from which the data is copied and pasted
        :updateview: is the function called when the main data is changed (paste/cut action)
        :param row0: is th first row of the grid where the clipborad sits
        :param col0: is th first column of the grid where the clipborad sits

        """
        self.root = root

        self.datawve = datawve
        self.updateview = updateview
        self.dataclpbrd = []
        self.clipboardtime = 0

        row = row0
        col = col0
        rowspan = 1
        colspan = 1
        self.tableclipboard = Table(root, self.dataclpbrd,  ('step', 'dt [s]', ('voltage [V]', VCOL), ('current [A]', CCOL)), row, col, CLIPROW, TABLECOL)

        row += CLIPROW+1
        col = col0
        colspan = 1
        insertlabelrow(root, row, col, ('beg step', None, 'end step'))
        self.ivarstepbeg = IntVar()
        self.ivarstepend = IntVar()
        insertentryrow(root, row, col, (None, self.ivarstepbeg, None, self.ivarstepend))
        col = col0+TABLECOL
        Button(root, text="Copy", command=self.butcmdcopy).grid(row=row, column=col, sticky=E+W, padx=8)
        col += colspan
        Button(root, text="Cut", command=self.butcmdcut).grid(row=row, column=col, sticky=E+W, padx=8)

        row += rowspan
        col = col0
        insertlabelrow(root, row, col, ('paste step', None, 'paste times'))
        self.ivarpastestep = IntVar()
        self.ivarpastetimes = IntVar()
        self.ivarpastetimes.set(1)
        insertentryrow(root, row, col, (None, self.ivarpastestep, None, self.ivarpastetimes))
        col = col0+TABLECOL
        Button(root, text="Paste Ins", command=self.butcmdpasteins).grid(row=row, column=col, sticky=E+W, padx=8)
        col += colspan
        Button(root, text="Paste Ovw", command=self.butcmdpasteovw).grid(row=row, column=col, sticky=E+W, padx=8)

        row += rowspan
        col = col0
        insertlabelrow(root, row, col, ('coef (t,v,c)', ))
        self.dvartcoeff = DoubleVar()
        self.dvarvcoeff = DoubleVar()
        self.dvarccoeff = DoubleVar()
        insertentryrow(root, row, col, (None, self.dvartcoeff, self.dvarvcoeff, self.dvarccoeff))
        col = col0+TABLECOL
        Button(root, text="Amp Clipb", command=self.butcmdampliclip).grid(row=row, column=col, sticky=E+W, padx=8)
        col += colspan
        Button(root, text="Trn Clipb", command=self.butcmdtransclip).grid(row=row, column=col, sticky=E+W, padx=8)

        row += rowspan
        col = col0
        insertlabelrow(root, row, col, ('rmp steps', ))
        self.ivarrampsteps = IntVar()
        self.ivarrampsteps.set(10)
        insertentryrow(root, row, col, (None, self.ivarrampsteps, None, None))
        col = col0+TABLECOL
        Button(root, text="Rmp Clipb", command=self.butcmdramp).grid(row=row, column=col, sticky=E+W, padx=8)

    def setbegin(self, r):
        """
        Set begin row from which operate.

        :param r: is the begin row (index) of the data from which copy/paste/cut will operate

        """

        if r < len(self.datawve):
            self.ivarstepbeg.set(r)
            self.ivarpastestep.set(r)

    def setend(self, r):
        """
        Set end row from which operate.

        :param r: is the end row (index) of the data from which copy/cut will operate

        """

        if r < len(self.datawve):
            self.ivarstepend.set(r)

    def butcmdcopy(self):
        """
        Copy from data (from begin to end) to clipboard. Timings in the clipboard are stored as delta.

        :returns: True if the operation was succseful

        """

        sb = self.ivarstepbeg.get()
        se = self.ivarstepend.get()

        if sb < 0 or sb >= len(self.datawve) or se < 0 or se >= len(self.datawve) or se < sb:
            return False

        del self.dataclpbrd[:]
        self.clipboardtime = 0

        if sb > 0:
            t0 = self.datawve[sb-1][0]
        else:
            t0 = 0
        t00 = t0

        for i in range(sb, se+1):
            lne = self.datawve[i]
            t1 = lne[0]
            self.dataclpbrd.append([t1-t0]+lne[1:])
            t0 = t1

        self.clipboardtime = t0-t00

        self.tableclipboard.updateview()

        return True

    def butcmdcut(self):
        """
        Cut from clipboard (begin to help) to data. Timings in the clipboard are stored as delta.

        :returns: True if the operation was succseful.

        """

        if not self.butcmdcopy():
            return False

        for i in range(self.ivarstepend.get()+1, len(self.datawve)):
            self.datawve[i][TPOS] -= self.clipboardtime

        sb = self.ivarstepbeg.get()
        for i in range(self.ivarstepend.get()-sb+1):
            del self.datawve[sb]

        self.tableclipboard.updateview()

        self.updateview()

        return True

    def paste(self):
        """
        Paste from clipboard to data (paste step). Timings in the data are restored as absolute timings.

        :returns: True if the operation was succseful

        """

        i = self.ivarpastestep.get()
        if i > 0:
            t0 = self.datawve[i-1][0]
        else:
            t0 = 0

        for t in range(self.ivarpastetimes.get()):
            for lne in self.dataclpbrd:
                t1 = lne[0]+t0
                self.datawve.insert(i, [t1]+lne[1:])
                i += 1
                t0 = t1

        return i

    def butcmdpasteins(self):
        """
        Paste from clipboard inserting into data (paste step). Timings in the data are restored as absolute timings.

        :returns: True if the operation was succseful

        """

        i = self.paste()

        dt = self.clipboardtime*self.ivarpastetimes.get()
        for i in range(i, len(self.datawve)):
            self.datawve[i][0] += dt

        self.updateview()

    def butcmdpasteovw(self):
        """
        Paste from clipboard overwriting data (paste step) with timings lower the clipboard data. Timings in the data are restored as absolute timings.

        :returns: True if the operation was succseful

        """
        i = self.paste()

        if i > 0:
            t0 = self.datawve[i-1][0]
        else:
            t0 = 0

        while i < len(self.datawve) and self.datawve[i][0] <= t0:
            del self.datawve[i]

        self.updateview()

    def butcmdampliclip(self):
        """
        Clipboard data is amplified (attenuated if factor is <1). Also timing can be alterated.
        """
        coeff = (self.dvartcoeff.get(), self.dvarvcoeff.get(), self.dvarccoeff.get())
        acc = 0
        for l in self.dataclpbrd:
            for i in range(3):
                l[i] *= coeff[i]
            acc += l[0]
        self.clipboardtime = acc

        self.tableclipboard.updateview()

    def butcmdtransclip(self):
        """
        Clipboard data is translated. Also timing can be translated since the timing is stored as relative only the first occurence is alered.

        :returns: True if the operation was succseful

        """

        if len(self.dataclpbrd) <= 0:
            return False

        self.dataclpbrd[0][TPOS] += self.dvartcoeff.get()

        self.clipboardtime += self.dvartcoeff.get()  # only the first occurency of time is updated
        coeff = (0, self.dvarvcoeff.get(), self.dvarccoeff.get())  # time is not traslated because stored as delta on the clipboard

        for l in self.dataclpbrd:
            for i in range(1, 3):
                l[i] += coeff[i]

        self.tableclipboard.updateview()

        return True

    def butcmdramp(self):
        """
        Clipboard first and last rows are used to make a ramp of given number of steps.

        :returns: True if the operation was succseful

        """

        if len(self.dataclpbrd) <= 0:
            return False

        beg = self.dataclpbrd[0][1:]
        end = self.dataclpbrd[-1][1:]
        steps = self.ivarrampsteps.get()-1
        deltastep = [(e-b)/steps for e, b in zip(end, beg)]
        tstep = (self.clipboardtime-self.dataclpbrd[0][0])/steps
        del self.dataclpbrd[1:]
        for s in range(steps):
            beg = [a+b for a, b in zip(beg, deltastep)]
            self.dataclpbrd.append([tstep]+beg)

        self.tableclipboard.updateview()

        return True


if __name__ == '__main__':
    from Tkinter import Tk

    root = Tk()
    points = []
    for r in range(1, 35):
        line = []
        for c in range(3):
            line.append(r*10+1.11*(c+1))
        points.append(line)

    my_gui = Clipboard(root, points, lambda: 0, 0, 0)
    root.mainloop()
