#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
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

        # Authenticate
        for i in range (0,63):
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, i, key, nuid)
            #Check if authenticated
            if status == MIFAREReader.MI_OK:
                MIFAREReader.MFRC522_Read(i)
            else:
                print "Authentication error"
        else:
            while True:
                CR = raw_input ("Do you want to read another card? (True/False) ")
                if CR == "True":   
                    continue_reading = True
                    break
                if CR == "False":
                    continue_reading = False
                    break

    
