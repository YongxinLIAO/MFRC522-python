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

def check(list):
    if not list[0] == 0:
        if list[0] == list[8]:
            if list[1] == list[9]:
                if list[2] == list[10]:
                    if list[3] == list[11]:
                        if int(list[0])+int(list[4])== 255:
                            if int(list[1])+int(list[5])== 255:
                                if int(list[2])+int(list[6])== 255:
                                    if int(list[3])+int(list[7])== 255:
                                        TF=True
                                        print "Checked"
                                    else:
                                        print "Error byte 7 is not the invered hexadecimal of byte 3"
                                        TF=False 
                                else:
                                    print "Error byte 6 is not the invered hexadecimal of byte 2"
                                    TF=False 
                            else:
                                print "Error byte 5 is not the invered hexadecimal of byte 1"
                                TF=False 
                        else:
                            print "Error byte 4 is not the invered hexadecimal of byte 0"
                            TF=False 
                    else:
                        print "Error byte 3 != byte 11"
                        TF=False
                else:
                    print "Error byte 2 != byte 10"
                    TF=False
            else:
                print "Error byte 1 != byte 9"
                TF=False
        else:
            print "Error byte 0 != byte 8"
            TF=False
    else:
        print "Checked"
        TF=True
    return TF

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

jump = 1

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    print "1"
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
        GroupMember = raw_input ("which group member's data do you want to read? (e, i,ii,iii)")
        L=[]
        if GroupMember == "e":        
            #Section 1 Block 0
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 4, key, nuid)
            if status == MIFAREReader.MI_OK:
                GetValueLine3=MIFAREReader.MFRC522_ReturnValue(4)
            else:
                print "Authentication error"

            #Section 1 Block 1
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 5, key, nuid)
            if status == MIFAREReader.MI_OK:
                GetValueLine2=MIFAREReader.MFRC522_ReturnValue(5)
            else:
                print "Authentication error"

            #Section 1 Block 2
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 6, key, nuid)
            if status == MIFAREReader.MI_OK:
                GetValueLine1=MIFAREReader.MFRC522_ReturnValue(6)
            else:
                print "Authentication error"

            #Section 2 Block 0
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, nuid)
            if status == MIFAREReader.MI_OK:
                GetValueLine4=MIFAREReader.MFRC522_ReturnValue(8)
            else:
                print "Authentication error"
                
            print "Section 1 Block 0"
            TFCheck1 = check(GetValueLine3)
            print "Section 1 Block 1"
            TFCheck2 = check(GetValueLine2)
            print "Section 1 Block 2"
            TFCheck3 = check(GetValueLine1)
            print "Section 2 Block 0"
            TFCheck4 = check(GetValueLine4)

            if  TFCheck1 and TFCheck2 and TFCheck3 and TFCheck4:
                i=3
                while i>=0:
                    if not GetValueLine1[i]== 0 :
                        L.append(GetValueLine1[i])
                    i=i-1
                i=3
                while i>=0:
                    if not GetValueLine2[i]== 0 :
                        L.append(GetValueLine2[i])
                    i=i-1
                i=3
                while i>=0:
                    if not GetValueLine3[i]== 0 :
                        L.append(GetValueLine3[i])
                    i=i-1
                n=''.join(chr(i) for i in L)
                #print L
                print "Name: " + n

                y=""
                k=3
                while k>=0:
                    if len(str(GetValueLine4[k]))== 1:
                        y = y + str("0")+str(hex(GetValueLine4[k])[2:])
                    else:
                        y = y + str(hex(GetValueLine4[k])[2:])
                    k=k-1
                print "Favorite Year: " + str(int(y,16))

        if GroupMember == "i":        
            #Section 3 Block 0
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 12, key, nuid)
            if status == MIFAREReader.MI_OK:
                GetValueLine3=MIFAREReader.MFRC522_ReturnValue(12)
            else:
                print "Authentication error"

            #Section 3 Block 1
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 13, key, nuid)
            if status == MIFAREReader.MI_OK:
                GetValueLine2=MIFAREReader.MFRC522_ReturnValue(13)
            else:
                print "Authentication error"

            #Section 3 Block 2
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 14, key, nuid)
            if status == MIFAREReader.MI_OK:
                GetValueLine1=MIFAREReader.MFRC522_ReturnValue(14)
            else:
                print "Authentication error"

            #Section 4 Block 0
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 16, key, nuid)
            if status == MIFAREReader.MI_OK:
                GetValueLine4=MIFAREReader.MFRC522_ReturnValue(16)
            else:
                print "Authentication error"

            print "Section 3 Block 0"
            TFCheck1 = check(GetValueLine3)
            print "Section 3 Block 1"
            TFCheck2 = check(GetValueLine2)
            print "Section 3 Block 2"
            TFCheck3 = check(GetValueLine1)
            print "Section 4 Block 0"
            TFCheck4 = check(GetValueLine4)

            if  TFCheck1 and TFCheck2 and TFCheck3 and TFCheck4:
                i=3
                while i>=0:
                    if not GetValueLine1[i]== 0 :
                        L.append(GetValueLine1[i])
                    i=i-1
                i=3
                while i>=0:
                    if not GetValueLine2[i]== 0 :
                        L.append(GetValueLine2[i])
                    i=i-1
                i=3
                while i>=0:
                    if not GetValueLine3[i]== 0 :
                        L.append(GetValueLine3[i])
                    i=i-1
                n=''.join(chr(i) for i in L)
                #print L
                print "Name: " + n

                y=""
                k=3
                while k>=0:
                    if len(str(GetValueLine4[k]))== 1:
                        y = y + str("0")+str(hex(GetValueLine4[k])[2:])
                    else:
                        y = y + str(hex(GetValueLine4[k])[2:])
                    k=k-1
                #print y
                print "Favorite Year: " + str(int(y,16))

        if GroupMember == "ii":        
            #Section 5 Block 0
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 20, key, nuid)
            if status == MIFAREReader.MI_OK:
                GetValueLine3=MIFAREReader.MFRC522_ReturnValue(20)
            else:
                print "Authentication error"

            #Section 5 Block 1
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 21, key, nuid)
            if status == MIFAREReader.MI_OK:
                GetValueLine2=MIFAREReader.MFRC522_ReturnValue(21)
            else:
                print "Authentication error"

            #Section 5 Block 2
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 22, key, nuid)
            if status == MIFAREReader.MI_OK:
                GetValueLine1=MIFAREReader.MFRC522_ReturnValue(22)
            else:
                print "Authentication error"

            #Section 6 Block 0
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 24, key, nuid)
            if status == MIFAREReader.MI_OK:
                GetValueLine4=MIFAREReader.MFRC522_ReturnValue(24)
            else:
                print "Authentication error"

            print "Section 5 Block 0"
            TFCheck1 = check(GetValueLine3)
            print "Section 5 Block 1"
            TFCheck2 = check(GetValueLine2)
            print "Section 5 Block 2"
            TFCheck3 = check(GetValueLine1)
            print "Section 6 Block 0"
            TFCheck4 = check(GetValueLine4)

            if  TFCheck1 and TFCheck2 and TFCheck3 and TFCheck4:
                i=3
                while i>=0:
                    if not GetValueLine1[i]== 0 :
                        L.append(GetValueLine1[i])
                    i=i-1
                i=3
                while i>=0:
                    if not GetValueLine2[i]== 0 :
                        L.append(GetValueLine2[i])
                    i=i-1
                i=3
                while i>=0:
                    if not GetValueLine3[i]== 0 :
                        L.append(GetValueLine3[i])
                    i=i-1
                n=''.join(chr(i) for i in L)
                #print L
                print "Name: " + n

                y=""
                k=3
                while k>=0:
                    if len(str(GetValueLine4[k]))== 1:
                        y = y + str("0")+str(hex(GetValueLine4[k])[2:])
                    else:
                        y = y + str(hex(GetValueLine4[k])[2:])
                    k=k-1
                #print y
                print "Favorite Year: " + str(int(y,16))

        if GroupMember == "iii":        
            #Section 7 Block 0
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 28, key, nuid)
            if status == MIFAREReader.MI_OK:
                GetValueLine3=MIFAREReader.MFRC522_ReturnValue(28)
            else:
                print "Authentication error"

            #Section 7 Block 1
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 29, key, nuid)
            if status == MIFAREReader.MI_OK:
                GetValueLine2=MIFAREReader.MFRC522_ReturnValue(29)
            else:
                print "Authentication error"

            #Section 7 Block 2
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 30, key, nuid)
            if status == MIFAREReader.MI_OK:
                GetValueLine1=MIFAREReader.MFRC522_ReturnValue(30)
            else:
                print "Authentication error"

            #Section 8 Block 0
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 32, key, nuid)
            if status == MIFAREReader.MI_OK:
                GetValueLine4=MIFAREReader.MFRC522_ReturnValue(32)
            else:
                print "Authentication error"

            print "Section 7 Block 0"
            TFCheck1 = check(GetValueLine3)
            print "Section 7 Block 1"
            TFCheck2 = check(GetValueLine2)
            print "Section 7 Block 2"
            TFCheck3 = check(GetValueLine1)
            print "Section 8 Block 0"
            TFCheck4 = check(GetValueLine4)

            if  TFCheck1 and TFCheck2 and TFCheck3 and TFCheck4:
                i=3
                while i>=0:
                    if not GetValueLine1[i]== 0 :
                        L.append(GetValueLine1[i])
                    i=i-1
                i=3
                while i>=0:
                    if not GetValueLine2[i]== 0 :
                        L.append(GetValueLine2[i])
                    i=i-1
                i=3
                while i>=0:
                    if not GetValueLine3[i]== 0 :
                        L.append(GetValueLine3[i])
                    i=i-1
                n=''.join(chr(i) for i in L)
                #print L
                print "Name: " + n

                y=""
                k=3
                while k>=0:
                    if len(str(GetValueLine4[k]))== 1:
                        y = y + str("0")+str(hex(GetValueLine4[k])[2:])
                    else:
                        y = y + str(hex(GetValueLine4[k])[2:])
                    k=k-1
                #print y
                print "Favorite Year: " + str(int(y,16))
            
    MIFAREReader.MFRC522_StopCrypto1()        
    if not(jump%2)==0:
        while True:
            CR = raw_input ("Do you want to read another card? (True/False) ")
            if CR == "True":   
                continue_reading = True
                break
            if CR == "False":
                continue_reading = False
                break
    jump = jump +1    
