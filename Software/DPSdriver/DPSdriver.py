#!/usr/bin/env python

"""
 DPS supplier serial driver
 (C)2019 - Simone Pernice - pernice@libero.it
  This is distributed under GNU LGPL license, see license.txt
"""

import serial

import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

def initialize_registers():
    """
    Initialize the register statically created for the class.

    :returns: the dictionary of the registers used by the class
    """
    reg = {
        'vset'   : (0x00, 'rw', 2, 'Voltage setting'),
        'iset'   : (0x01, 'rw', 2, 'Current setting'),
        'vout'   : (0x02, 'r', 2, 'Output voltage'),
        'iout'   : (0x03, 'r', 2, 'Output current'),
        'pout'   : (0x04, 'r', 2, 'Output power'),
        'vinp'   : (0x05, 'r', 2, 'Input voltage'),
        'lock'   : (0x06, 'rw', 0, 'Key lock: 0 is not lock, 1 is locked'),
        'prot'   : (0x07, 'r', 0, 'Protection status: 0 OK, 1 is over voltage protection, 2 over current protection, 3 over power protection'),
        'cvcc'   : (0x08, 'r', 0, 'Constant voltage or current status: 0 constant voltage, 1 constant current'),
        'onoff' : (0x09, 'rw', 0, 'Switch output status: 0 off , 1 on'),
        'bled'   : (0x0A, 'rw', 0, 'Backlight brightness level: 0 darkest, 5 brightest'),
        'model' : (0x0B, 'r', 0, 'Product model'),
        'fware' : (0x0C, 'r', 0, 'Firmware version'),
        'mSet'   : (0x23, 'rw', 0, 'Set the required meomory as active data group')
    }

    memreg = {
        'vset'  : (0x50, 'rw', 2, ' voltage setting'),
        'iset'  : (0x51, 'rw', 2, ' current setting'),
        'ovp'    : (0x52, 'rw', 2, ' over voltage protection'),
        'ocp'    : (0x53, 'rw', 2, ' over current protection'),
        'opp'    : (0x54, 'rw', 1, ' over power protection'),
        'bled'  : (0x55, 'rw', 0, ' backlight brightness level: 0 darkest, 5 brightest'),
        'pre'  : (0x56, 'rw', 0, ' preset number'),
        'onoff': (0x57, 'rw', 0, ' switch output status: 0 off , 1 on'),
    }

    for i in range(10):
        for mreg in memreg:
            v = memreg[mreg]
            nv = [v[0]+i*0x10]
            for j in range(1, len(v)-1):
                nv.append(v[j])
            nv.append('Memory '+str(i)+v[-1])
            reg['m'+str(i)+mreg] = tuple(nv)

    return reg


class DPSdriver():
    """
    DSPdriver is a class to link to a DPS supplier. It allow to read or write single or multimple registers called by name.
    """
    REGISTERS = initialize_registers()

    #port is the serial port where the converter is linked to
    #address is the supplier address as far as I know they are all address 0x01
    def __init__(self, port, address=0x01):
        """
        Create a DSP driver instance to read and write the DSP registers.

        :param port: is the string with the prot name i.e. /dev/ttyUSB0 or COM5 for Windows
        :param address: is the address of DPS supplier usually they all have address 1
        :raises ValueError: if it cannot open the serial port or link to the supplier
        """
        self.address = address

        try:
            s = serial.Serial(port, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
        except Exception as e:
            raise ValueError('It was not possible to open the serial port '+str(e))

        try:
            self.master = modbus_rtu.RtuMaster(s)
        except Exception as e:
            raise ValueError('It was not possible to link to the power supplier '+str(e))

        self.master.set_timeout(5.0)
        self.master.set_verbose(True)

    def ___del___(self):
        self.master.__del__()

    def get(self, reglist):
        """
        Read the list of registers in reglist.
        Internally the sequence of registers is reordered to collect continguous registers in a single call.
        Reducing the number of calls make the function faster.

        :param reglist: is the list with the string of register names to be read
        :returns: the list of values read
        :raises NameError: if any of the register names is not foud
        :raises MemoryError: if any of the required registers is not readable
        """

        #Create the list of addresses to get from device
        adrdgt = []
        for reg in reglist:
            if reg not in DPSdriver.REGISTERS:
                raise NameError('The register '+reg+' is not known.')
            r = DPSdriver.REGISTERS[reg]
            if 'r' not in r[1]:
                raise MemoryError('The register '+reg+' is not readable, therefore get is not allowed.')
            adrdgt .append((r[0], r[2]))

        #Sort the registers in order to collect all the calls for adiacent register in only one to make it faster
        adrdgtsrt = sorted(adrdgt)
        nreg = 0
        dgts = []
        red = []
        baseadd = 0
        for ad in adrdgtsrt:
            if nreg > 0 and ad[0] != baseadd+nreg:
                v = self.master.execute(self.address, cst.READ_HOLDING_REGISTERS, baseadd, nreg)
                red += [todecimal(va, d) for va, d in zip(v, dgts)]
                nreg = 0

            if nreg == 0:
                baseadd = ad[0]
                dgts = []

            nreg += 1
            dgts.append(ad[1])

        v = self.master.execute(self.address, cst.READ_HOLDING_REGISTERS, baseadd, nreg)
        red += [todecimal(va, r[2]) for va, d in zip(v, dgts)]

        #reorder the result as for the caller registers order
        if adrdgt != adrdgtsrt:
            rslt = [0] * len(red)
            for v, a in zip(red, adrdgtsrt):
                rslt[adrdgt.index(a)] = v
        else:
            rslt = v

        return rslt

    def set(self, reglist, vallist):
        """
        Write the list of registers in reglist with the values in vallist.
        Internally the sequence of registers is reordered to collect continguous register in a single write call.
        Reducing the number of calls make the function much faster.

        :param reglist: is the list with the string of register names to be read
        :param vallist: is the list with the values to write in the registers
        :returns: the list of values read after the write function
        :raises NameError: if any of the register names is not found
        :raises MemoryError: if any of the required registers is not readable
        """

        #Create the list of addresses to get from device
        adrdgtval = []
        for reg, v in zip(reglist, vallist):
            if reg not in DPSdriver.REGISTERS:
                raise NameError('The register '+reg+' is not known.')
            r = DPSdriver.REGISTERS[reg]
            if 'w' not in r[1]:
                raise MemoryError('The register '+reg+' is not writable, therefore set is not allowed.')
            adrdgtval .append((r[0], r[2], tointeger(v, r[2])))

        #Sort the registers in order to collect all the calls for adiacent register in only one to make it faster
        adrdgtvalsrt = sorted(adrdgtval)
        nreg = 0
        dgts = []
        wrt = []
        red = []
        baseadd = 0
        for ad in adrdgtvalsrt:
            if nreg > 0 and ad[0] != baseadd+nreg:
                if nreg == 1:
                    v = self.master.execute(self.address, cst.WRITE_SINGLE_REGISTER, baseadd, 1, output_value=wrt[0])[1:-1]
                else:
                    v = self.master.execute(self.address, cst.WRITE_MULTIPLE_REGISTERS, baseadd, nreg, output_value=wrt)[len(wrt):-1]

                red += [todecimal(va, d) for va, d in zip(v, dgts)]
                nreg = 0

            if nreg == 0:
                baseadd = ad[0]
                dgts = []
                wrt = []

            nreg += 1
            dgts.append(ad[1])
            wrt.append(ad[2])

            if nreg == 1:
                v = self.master.execute(self.address, cst.WRITE_SINGLE_REGISTER, baseadd, 1, output_value=wrt[0])[1:-1]
            else:
                v = self.master.execute(self.address, cst.WRITE_MULTIPLE_REGISTERS, baseadd, nreg, output_value=wrt)[len(wrt):-1]

            red += [todecimal(va, d) for va, d in zip(v, dgts)]

        #reorder the result as for the caller registers order
        if adrdgtval != adrdgtvalsrt:
            rslt = [0] * len(red)
            for v, a in zip(red, adrdgtvalsrt):
                rslt[adrdgtval.index(a)] = v
        else:
            rslt = v

        return rslt

def list_registers():
    """
    Provide a list with the name of all registers available. Those names can be used in set and get.

    :returns: a list with the name of all registers known
    """
    return DPSdriver.REGISTERS.keys()

def help_register(reg):
    """
    Provide help on a register.

    :param reg: the register name whose function is require
    :returns: a string with register: name, address, type (read/write), decimal digits, function.
    :raises NameError: if the register name is not known
    """
    if reg not in DPSdriver.REGISTERS:
        raise NameError('The given register is not known')
    r = DPSdriver.REGISTERS[reg]
    h = 'Register: '+reg
    h += ', address: '+str(r[0])
    h += ', type: '+str(r[1])
    h += ', decimal digits: '+str(r[2])
    h += ', function: '+str(r[3])
    return h

def todecimal(val, digits):
    """
    Convert an integer number to decimal
    Used internally to convert number received by DPS in decimal

    :param val: is the integer value to convert in decimal
    :param digits: is the number of decimal digits to use
    :returns: the decimal (float) converted number
    """
    if digits == 0:
        return val
    d = digits
    while digits > 0:
        val /= 10.
        digits -= 1
    return round(val, d)

def tointeger(val, digits):
    """
    Convert a decimal number (float in Python) to integer
    Used internally to convert number from user to be sent to  DPS

    :param val: is the decimal value to convert to integer
    :param digits: is the number of decimal digits to use for integer conversion
    :returns: the integer coverted number
    """

    while digits > 0:
        val *= 10.
        digits -= 1
    return int(round(val))

def memorymap():
    """
    Provide a list with the memory map of the DPS.
    The lists is made by tuples with registers: (address, name, function explanation)

    :returns: a list with the name of all registers known
    """
    mm = []
    for r in DPSdriver.REGISTERS:
        val = DPSdriver.REGISTERS[r]
        mm.append(val[0], r, val[1], val[3])
    return mm.sort()

if __name__ == "__main__":
    DPS = DPSdriver('/dev/ttyUSB0')
#    print DPS.get('vInp')
    print DPS.get('model')
    print DPS.get('fware')
    print DPS.set('vSet', 4.54)
    print DPS.get('vSet')
    print DPS.set('vSet', 4.55)
    print DPS.get('vSet')
    print DPS.set('vSet', 4.56)
    print DPS.get('vSet')
    print DPS.set('vSet', 4.57)
    print DPS.get('vSet')
#    print DPS.set('vSet',  10.04)
#    print DPS.set('iSet',  0.12)
#    print DPS.set('onoff',  0)
#    print DPS.get('lock')
#    print DPS.set('lock',  1)
#    print DPS.get('vOut')
#    print DPS.get('iOut')
#    print DPS.set('bled', 0)
