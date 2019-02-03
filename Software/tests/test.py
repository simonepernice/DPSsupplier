#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""
 Modbus TestKit: Implementation of Modbus protocol in python
 (C)2009 - Luc Jean - luc.jean@gmail.com
 (C)2009 - Apidev - http://www.apidev.fr
 This is distributed under GNU LGPL license, see license.txt
"""

import serial

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

PORT = '/dev/ttyUSB0'

def main():
    """main"""
#    logger = modbus_tk.utils.create_logger("console")

    try:
        #Connect to the slave
        master = modbus_rtu.RtuMaster(
            serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
        )
        master.set_timeout(5.0)
        master.set_verbose(True)
#        logger.info("connected")

#        logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 3))
        voltSetRegister = 0x00        
        volt = 5.01
#        logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, voltSetRegister, 1))
#        logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, voltSetRegister, 1,  output_value=int (volt*100)))
#        logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, voltSetRegister, 1))
        
        print ('Read setting voltage '+str(master.execute(1, cst.READ_HOLDING_REGISTERS, voltSetRegister,  16)[0]/100.))
        print ('Write setting voltage ' +str(master.execute(1, cst.WRITE_SINGLE_REGISTER, voltSetRegister, 16,   output_value=int (volt*100))[1]/100.))
        print ('Read setting voltage '+str(master.execute(1, cst.READ_HOLDING_REGISTERS, voltSetRegister,  16)[0]/100.))
        
        currSetRegister = 0x01       
        curr = 1.23 
        
        print ('Read setting current  '+str(master.execute(1, cst.READ_HOLDING_REGISTERS, currSetRegister, 16)[0]/100.))
        print ('Write setting current ' +str(master.execute(1, cst.WRITE_SINGLE_REGISTER, currSetRegister, 16,  output_value=int (curr*100))[1]/100.))
        print ('Read setting current  '+str(master.execute(1, cst.READ_HOLDING_REGISTERS, currSetRegister, 16)[0]/100.))        
        
        outVoltRegister = 0x02    
        print ('Read output voltage '+str(master.execute(1, cst.READ_HOLDING_REGISTERS, outVoltRegister, 16)[0]/100.))
        
        outCurrRegister = 0x03    
        print ('Read output current '+str(master.execute(1, cst.READ_HOLDING_REGISTERS, outCurrRegister , 16)[0]/100.))
        
        outPowrRegister = 0x04    
        print ('Read output power '+str(master.execute(1, cst.READ_HOLDING_REGISTERS, outPowrRegister , 16)[0]))
               
        inpVoltRegister = 0x05    
        print ('Read input voltage '+str(master.execute(1, cst.READ_HOLDING_REGISTERS, inpVoltRegister, 16)[0]/100.))
        
#        return
        
        outSwitchRegister = 0x09
        osw = 1
        print ('Read output switch '+str(master.execute(1, cst.READ_HOLDING_REGISTERS, outSwitchRegister , 16)[0]))
        print ('Write setting current ' +str(master.execute(1, cst.WRITE_SINGLE_REGISTER, outSwitchRegister, 16,  output_value=osw )[1]))
        
        for volt in range (1,  10,  1) :
            print ('Write setting voltage ' +str(master.execute(1, cst.WRITE_SINGLE_REGISTER, voltSetRegister, 16,  output_value=int (volt*100))[1]/100.))
        
        for volt in range (10,  1,  -1) :
            print ('Write setting voltage ' +str(master.execute(1, cst.WRITE_SINGLE_REGISTER, voltSetRegister, 16,  output_value=int (volt*100))[1]/100.))
            
        #again without prints
        for volt in range (1,  10,  1) :
            master.execute(1, cst.WRITE_SINGLE_REGISTER, voltSetRegister, 16,  output_value=int (volt*100))
        
        for volt in range (10,  1,  -1) :
            master.execute(1, cst.WRITE_SINGLE_REGISTER, voltSetRegister, 16,  output_value=int (volt*100))
            

        
#        logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, currSetRegister, 1))
#        logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, currSetRegister, 1,  output_value=int (curr*100)))
#        logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, currSetRegister, 1))        
        
#        logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0x01, 2))
#        logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, 0x01, 2,  output_value=100))
#        logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0x01, 2))
        
                

        #send some queries
        #logger.info(master.execute(1, cst.READ_COILS, 0, 10))
        #logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 8))
        #logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 100, 3))
#        logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0x00, 1))
        #logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 0x007, output_value=5))
#        logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, 0x00, output_value=5))
#        logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0x00, 1))
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 0, 1, 1, 0, 1, 1]))
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 100, output_value=xrange(12)))

    except modbus_tk.modbus.ModbusError as exc:
#        logger.error("%s- Code=%d", exc, exc.get_exception_code())
        print ('Exception: '+str(exc))

if __name__ == "__main__":
    main()
