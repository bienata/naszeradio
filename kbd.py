import RPi.GPIO as GPIO
import subprocess
import time
import os
import socket 

KEY_SKIP    = 13        # SKIPNEXT
KEY_NEXT    = 15        # SEARCHNEXT
KEY_START   = 23        # START
KEY_RESET   = 21        # BTN_0
KEY_STOP    = 19        # STOP
#KEY_OUTS    = 8         # STANDBY
KEY_OUTS    = 7         # STANDBY
#--------------------------------------------------------------                
def onKeyPressed( channel ):
    if GPIO.input( channel ) == True: return 
    time.sleep( 0.5 )
    BUTTON_TEMP_FILE = "/tmp/remote_key.txt"
    keyMapping = { KEY_SKIP : "SKIPNEXT", KEY_NEXT : "SEARCHNEXT", KEY_START : "START", KEY_RESET : "BTN_0", KEY_STOP : "STOP", KEY_OUTS : "STANDBY" }
    file = open( BUTTON_TEMP_FILE, "w" )
    file.write( keyMapping[ channel ] )
    file.close()
    print ( str(channel) + " " + keyMapping[ channel ] )    
#--------------------------------------------------------------                
# program glowny    
GPIO.setwarnings( False )
GPIO.setmode( GPIO.BOARD )
GPIO.setup( KEY_SKIP,   GPIO.IN, pull_up_down = GPIO.PUD_UP )      
GPIO.setup( KEY_NEXT,   GPIO.IN, pull_up_down = GPIO.PUD_UP )      
GPIO.setup( KEY_STOP,   GPIO.IN, pull_up_down = GPIO.PUD_UP )     
GPIO.setup( KEY_START,  GPIO.IN, pull_up_down = GPIO.PUD_UP )     
GPIO.setup( KEY_RESET,  GPIO.IN, pull_up_down = GPIO.PUD_UP )
GPIO.setup( KEY_OUTS,   GPIO.IN, pull_up_down = GPIO.PUD_UP )     
GPIO.add_event_detect( KEY_SKIP , GPIO.FALLING, callback = onKeyPressed )
GPIO.add_event_detect( KEY_NEXT , GPIO.FALLING, callback = onKeyPressed )
GPIO.add_event_detect( KEY_STOP , GPIO.FALLING, callback = onKeyPressed )  
GPIO.add_event_detect( KEY_START, GPIO.FALLING, callback = onKeyPressed )  
GPIO.add_event_detect( KEY_RESET, GPIO.FALLING, callback = onKeyPressed )
GPIO.add_event_detect( KEY_OUTS,  GPIO.FALLING, callback = onKeyPressed )  

while True:    
    time.sleep( 0.1 )        

#fin    
