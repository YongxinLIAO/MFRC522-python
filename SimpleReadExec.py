#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

continue_reading = True
cardId = "empty"

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
    # if status == MIFAREReader.MI_OK:
        #print "Card detected"
        
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
        

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        data = ""+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
        if cardId!=data:
            cardId = data
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send(cardId)
           # data = s.recv(BUFFER_SIZE)
           # s.close()

           # print "received data:", data

            # Print UID
            print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
            
