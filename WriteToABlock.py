#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import re
import sys

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()
    sys.exit()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

jump = 1
# This loop keeps checking for chips. If one is near it will get the NUID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    
    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
   
    # Get the NUID of the card
    (status,nuid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the NUID, continue
    if status == MIFAREReader.MI_OK:

        NUID16 = []
        # Print NUID
        for j in range (0,4):
            if len(str(nuid[j]))== 1:
                NUID16.append(str("0")+str(hex(nuid[j]))[2:])
            else:
                NUID16.append(str(hex(nuid[j]))[2:])

        print "Card read NUID: "+str(NUID16[0])+","+str(NUID16[1])+","+str(NUID16[2])+","+str(NUID16[3])
    
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(nuid)

        Sector = 16
        Block = 4
        while not int(Sector) in range (0,15):
            Sector = input ("Which Sector do you want to write? (0~15)")
        while not int(Block) in range (0,3):
            Block = input ("Which Block in Sector " + str(Sector) + " do you want to write? (0~3)")

        location = Sector * 4 + Block
        print location

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, location, key, nuid)
        print "\n"

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            
            print "Sector " + str(Sector) + " Block " + str(Block) + " looked like this:"
            # Read block 8
            MIFAREReader.MFRC522_Read(location)
            print "\n"

            data10 = []
            # Variable for the data to write
            i=0
            while i<16:
                data = raw_input ("New value of byte " + str(i) + " (00~ff): ")
                #
               
                if not re.match (r"\d|[a-f]|[A-F]", data):
                    print "Error, the value should be within (00~ff)"
                else:
                    if len(data)>2:
                        print "Error, the value should be within (00~ff)"
                    else:
                        i=i+1
                        data10.append(int(str(data),16))

            print "\n"  
            print "Sector " + str(Sector) + " Block " + str(Block) +  "will now be filled with new data:"
            # Write the data
            MIFAREReader.MFRC522_Write(location, data10)
            print "\n"

            print "It now looks like this:"
            # Check to see if it was written
            MIFAREReader.MFRC522_Read(location)
            print "\n"

            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print "Authentication error"    
    
   
    if not(jump%2)==0:
        while True:
            CR = raw_input ("Do you want to write another Data? (True/False) ")
            if CR == "True":   
                continue_reading = True
                break
            if CR == "False":
                continue_reading = False
                break
    jump = jump +1
  
