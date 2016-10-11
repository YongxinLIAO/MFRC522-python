#!/usr/bin/python
# This is only executed on the device client e.g. Raspberry Pi
import time
import os, json
import ibmiotf.application
import uuid
import SimpleRead



client = None


try:
  options = ibmiotf.application.ParseConfigFile("/home/pi/device.cfg")
  options["deviceId"] = options["id"]
  options["id"] = "aaa" + options["id"]
  client = ibmiotf.application.Client(options)
  print "try to connect to IoT"
  client.connect()
  print "connect to IoT successfully"


  while True:
    RFIDData = SimpleRead.sample()
    jsonRFIDData = json.dumps(RFIDData)
    client.publishEvent("raspberrypi", options["deviceId"], "RFIDSensor", "json", jsonRFIDData)
    print "Even Published"
    time.sleep(2)
 
except ibmiotf.ConnectionException as e:
 print e
