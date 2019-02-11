#!/usr/bin/env python

"""
 DPS serial driver 
 (C)2019 - Simone Pernice - pernice@libero.it
  This is distributed under GNU LGPL license, see license.txt
"""

import serial
#import modbus_tk

import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

class DPSdriver () :
    REGISTERS = {
        'vSet'   : (0x00,  'rw',    2,  'Voltage setting'), 
        'iSet'   : (0x01,  'rw',    2,  'Current setting'), 
        'vOut'   : (0x02,  'r',      2,   'Output voltage'), 
        'iOut'   : (0x03,  'r',      2,   'Output current'), 
        'pOut'   : (0x04,  'r',      2,   'Output power'), 
        'vInp'   : (0x05,  'r',      2,   'Input voltage'), 
        'lock'   : (0x06,  'rw',    0,   'Key lock: 0 is not lock, 1 is locked'  ), 
        'prot'   : (0x07,  'r',      0,   'Protection status: 0 OK, 1 is over voltage protection, 2 over current protection, 3 over power protection'  ), 
        'cvcc'   : (0x08,  'r',      0,   'Constant voltage or current status: 0 constant voltage, 1 constant current'  ), 
        'onoff' : (0x09,  'rw',    0,   'Switch output states: 0 off , 1 on'  ), 
        'bled'   : (0x0A,  'rw',    0,   'Backlight brightness level: 0 darkest, 5 brightest'  ), 
        'model' : (0x0B,  'r',      0,   'Product model'), 
        'fware' : (0x0C,  'r',      0,   'Firmware version'  ), 
        'gSet'   : (0x23,   'grw',  0,   'Set as active the required data group ') ,         
        'gvSet'  : (0x50,  'grw',  2,  'Voltage setting'), 
        'giSet'  : (0x51,  'grw',  2,  'Current setting'), 
        'govp'    : (0x52,  'grw',  2,  'Over voltage protection'), 
        'gocp'    : (0x53,  'grw',  2,  'Over current protection'), 
        'gopp'    : (0x54,  'grw',  1,  'Over power protection'), 
        'gbled'  : (0x55,  'grw',  0,  'Backlight brightness level: 0 darkest, 5 brightest'  ), 
        'gmPre'  : (0x56,  'grw',  0,  'Memory preset number'), 
        'gonoff': (0x57,  'grw',  0,  'Switch output states: 0 off , 1 on'  ),         
    }    

    #port is the serial port where the converter is linked to
    def __init__ (self,  port,  address=1):
        self.address = address

        try :
            s = serial.Serial(port, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
        except Exception as e :
            raise Exception ('It was not possible to open the given serial port '+str(e))
            
        try:
            self.master = modbus_rtu.RtuMaster(s)
        except Exception as e:
            raise Exception ('It was not possible to link to the power supplier '+str(e))
            
        self.master.set_timeout(5.0)
        self.master.set_verbose(True)  
        
    def ___del___ (self):
        self.master.__del__()

    def get (self,  reg,  group = 0) :
        if reg not in DPSdriver.REGISTERS : raise Exception ('The given register is not known')
        r = DPSdriver.REGISTERS[reg]        
        if 'r' not in r[1] : raise Exception ('The giver register is not readable, therefore get is not allowed')        
        regAddress = r[0]
        if group != 0 :
            if 'g' not in r[1] : raise Exception ('The given register is not part of a memory group, therefore memory group cannot be specified')
            regAddress += 0x10 * group
        v = self.master.execute(self.address, cst.READ_HOLDING_REGISTERS, regAddress,  1) 
        return self.toDecimal (v[0],  r[2])
        
    def set  (self,  reg,  val,  group = 0) :
        if reg not in DPSdriver.REGISTERS : raise Exception ('The given register is not known')
        r = DPSdriver.REGISTERS[reg]    
        if 'w' not in r[1] : raise Exception ('The giver register is not writeable, therefore set is not allowed')
        regAddress = r[0]
        if group != 0 :
            if 'g' not in r[1] : raise Exception ('The given register is not part of a memory group, therefore memory group cannot be specified')
            regAddress += 0x10 * group        
        v = self.master.execute(self.address, cst.WRITE_SINGLE_REGISTER, regAddress,  1,  output_value = self.toInteger(val,  r[2]))
        return self.toDecimal(v[1],  r[2])
        
    def toDecimal (self,  val,  digits) :
        if digits == 0:
            return val
        d = digits
        while digits > 0 :
            val /= 10.
            digits -= 1
        return round(val,  d)
        
    def toInteger (self,  val,  digits):
        while digits > 0:
            val *= 10.
            digits -= 1
        return int (round(val))
        
    def listRegisters (self):
        return DPSdriver.REGISTERS.keys()
        
    def help (self,  reg) :
        if reg not in DPSdriver.REGISTERS : raise Exception ('The given register is not known')
        r = DPSdriver.REGISTERS[reg]
        h =  'Register: '+reg
        h += ', address: '+str(r[0])
        h += ', type: '+str(r[1])
        h += ', decimal digits: '+str(r[2])
        h += ', function: '+str(r[3])
        return h

if __name__ == "__main__":
    dps =DPSdriver('/dev/ttyUSB0')
#    print dps.get('vInp')
    print dps.get('model')
    print dps.get('fware')
    print dps.set('vSet',  4.54)
    print dps.get('vSet')
    print dps.set('vSet',  4.55)
    print dps.get('vSet')
    print dps.set('vSet',  4.56)
    print dps.get('vSet')
    print dps.set('vSet',  4.57)
    print dps.get('vSet')
#    print dps.set('vSet',  10.04)
#    print dps.set('iSet',  0.12)
#    print dps.set('onoff',  0)
#    print dps.get('lock')
#    print dps.set('lock',  1)
#    print dps.get('vOut')
#    print dps.get('iOut')    
#    print dps.set('bled', 0)

