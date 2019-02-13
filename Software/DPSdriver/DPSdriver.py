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

def initializeRegisters () :
    reg = {
        'vset'   : (0x00,  'rw',    2,  'Voltage setting'), 
        'iset'   : (0x01,  'rw',    2,  'Current setting'), 
        'vout'   : (0x02,  'r',      2,   'Output voltage'), 
        'iout'   : (0x03,  'r',      2,   'Output current'), 
        'pout'   : (0x04,  'r',      2,   'Output power'), 
        'vinp'   : (0x05,  'r',      2,   'Input voltage'), 
        'lock'   : (0x06,  'rw',    0,   'Key lock: 0 is not lock, 1 is locked'  ), 
        'prot'   : (0x07,  'r',      0,   'Protection status: 0 OK, 1 is over voltage protection, 2 over current protection, 3 over power protection'  ), 
        'cvcc'   : (0x08,  'r',      0,   'Constant voltage or current status: 0 constant voltage, 1 constant current'  ), 
        'onoff' : (0x09,  'rw',    0,   'Switch output status: 0 off , 1 on'  ), 
        'bled'   : (0x0A,  'rw',    0,   'Backlight brightness level: 0 darkest, 5 brightest'  ), 
        'model' : (0x0B,  'r',      0,   'Product model'), 
        'fware' : (0x0C,  'r',      0,   'Firmware version'  ), 
        'mSet'   : (0x23,   'rw',  0,   'Set as active the required meomory data group ')
    }

    memReg = {  
        'vset'  : (0x50,  'rw',  2,  ' voltage setting'), 
        'iset'  : (0x51,  'rw',  2,  ' current setting'), 
        'ovp'    : (0x52,  'rw',  2,  ' over voltage protection'), 
        'ocp'    : (0x53,  'rw',  2,  ' over current protection'), 
        'opp'    : (0x54,  'rw',  1,  ' over power protection'), 
        'bled'  : (0x55,  'rw',  0,  ' backlight brightness level: 0 darkest, 5 brightest'  ), 
        'pre'  : (0x56,  'rw',  0,  ' preset number'), 
        'onoff': (0x57,  'rw',  0,  ' switch output status: 0 off , 1 on'  ),         
    }
   
   for i in range (10) :
       for mreg in memReg :
           v = mem[mreg]
           nv = [v[0]+i*0x10]
           for j in range (1, len(v)-1) :
               nv.append(v[j])
           nv.append('Memory '+str(i)+v[-1]))
           reg['m'+str(i)+mreg] = tuple (nv)
        
    return reg       
       

class DPSdriver () :
    REGISTERS = initializeRegisters()

    #port is the serial port where the converter is linked to
    #address is the supplier address as far as I know they are all address 0x01
    def __init__ (self,  port,  address=0x01):
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

    def get (self,  reg,  nreg = 1) :
        if reg not in DPSdriver.REGISTERS : raise Exception ('The given register is not known')
        r = DPSdriver.REGISTERS[reg]        
        if 'r' not in r[1] : raise Exception ('The giver register is not readable, therefore get is not allowed')        
        regAddress = r[0]
        v = self.master.execute(self.address, cst.READ_HOLDING_REGISTERS, regAddress,  nreg) 
        if nreg == 1 : return self.toDecimal (v[0], r[2])
        return [self.toDecimal (val, r[2]) for val in v]
        
    def set  (self,  reg,  val,  nreg = 1) :
        if reg not in DPSdriver.REGISTERS : raise Exception ('The given register is not known')
        r = DPSdriver.REGISTERS[reg]    
        if 'w' not in r[1] : raise Exception ('The giver register is not writeable, therefore set is not allowed')
        regAddress = r[0]     
        if nreg == 1:
            v = self.master.execute(self.address, cst.WRITE_SINGLE_REGISTER, regAddress,  1,  output_value = self.toInteger(val,  r[2]))
        else :
            v = self.master.execute(self.address, cst.WRITE_MULTIPLE_REGISTER, regAddress,  nreg,  output_value = [self.toInteger(v,  r[2]) for v in val]) 
        if nreg == 1 : return self.toDecimal(v[1],  r[2])
        return [self.toDecimal (val, r[2]) for val in v[1:-1]]
        
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
       
   def memoryMap (self) :
       mm = []
       for r in DPSdriver.REGISTERS :
           val =  DPSdriver.REGISTERS[r]
           adr = val[0]
           i = 0
           for i in range (len(mm)) :
               if adr < mm[i][0] : break
           mm.insert(i,(adr, r, val[1], val[3]))
       return mm

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

