#!/usr/bin/env python
# -*- coding: utf8 -*-

#---------------------------------------------------------------------------# 
# import the RFID Reaing libraries we need
#---------------------------------------------------------------------------# 

import RPi.GPIO as GPIO
import MFRC522
import signal


#---------------------------------------------------------------------------# 
# import the modbus libraries we need
#---------------------------------------------------------------------------# 
import thread
import time
from pymodbus.server.async import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer

#---------------------------------------------------------------------------# 
# import the twisted libraries we need
#---------------------------------------------------------------------------# 
from twisted.internet.task import LoopingCall


#---------------------------------------------------------------------------# 
# initialize your data store
#---------------------------------------------------------------------------# 
store = ModbusSlaveContext(
    co = ModbusSequentialDataBlock(0x01, [1]*100),
    di = ModbusSequentialDataBlock(0x01, [0]*100), 
    hr = ModbusSequentialDataBlock(0x01, [1]*100),
    ir = ModbusSequentialDataBlock(0x01, [4]*100))
context = ModbusServerContext(slaves=store, single=True)


#---------------------------------------------------------------------------# 
# initialize the server information
#---------------------------------------------------------------------------# 
identity = ModbusDeviceIdentification()
identity.VendorName  = 'pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl   = 'http://github.com/bashwork/pymodbus/'
identity.ProductName = 'pymodbus Server'
identity.ModelName   = 'pymodbus Server'
identity.MajorMinorRevision = '1.0'

#====================================================

# Reading X and Y from RFID Tag

#====================================================
def updating_positions(a):
    register = 3
    slave_id = 0x01
    address1  = 0x01
    address2  = 0x02
    address3  = 0x03
    
    continue_reading = True
        
    MIFAREReader = MFRC522.MFRC522()
        
    while continue_reading:
        
        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print "Card detected"
        
        # Get the UID of the card
            (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
            if status == MIFAREReader.MI_OK:

            # Print UID
                print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
        
            # This is the default key for authentication
                key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
            
            # Select the scanned tag
                MIFAREReader.MFRC522_SelectTag(uid)

            # Authenticate
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
        
            # Check if authenticated
                data=[]
            if status == MIFAREReader.MI_OK:
                data=MIFAREReader.MFRC522_Read(8)
                value1 = [data[0]]
                print "X=" + str(data[0])
                context[slave_id].setValues(register, address1, value1)
                
                value2 = [data[1]]
                print "Y=" + str(data[1])
                context[slave_id].setValues(register, address2, value2)
                
                value3   = [1]
                print "Now UR5 is Moving "+ str(value3)
                context[slave_id].setValues(register, address3, value3)
                
                MIFAREReader.MFRC522_StopCrypto1()
            else:
                    print "Authentication error"

            continue_reading=input("Do you want to raed a RFID Tag? (True or False)")
            value4   = [0]
            context[slave_id].setValues(register, address3, value4)
            print "Ready to Move "+ str(value4)
            
#---------------------------------------------------------------------------# 
# run the server you want
#---------------------------------------------------------------------------#
thread.start_new_thread(updating_positions,(context,))
StartTcpServer(context, identity=identity, address=("169.254.184.72", 502))


