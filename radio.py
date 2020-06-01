from datetime import datetime
from RPLCD import CharLCD
import RPi.GPIO as GPIO
from pathlib import Path
import subprocess
import time
import os
import socket 
#-------------------------------------------------------------------------------------
SDD_STORAGE = "/mnt/usb_hdd_1/MP3"
BUTTON_TEMP_FILE = "/tmp/remote_key.txt"
# pelna sciezka do mnie, to na potrzeby serwisu
def myFolder():
    return str( Path(__file__).resolve().parent )
#-------------------------------------------------------------------------------------
# aktualne IP radia
def getCurrentIp():
    return subprocess.run( [ myFolder() + '/myip.sh'], stdout=subprocess.PIPE ).stdout.decode('utf-8').splitlines()[0]
#-------------------------------------------------------------------------------------
def checkIrButtons():
    if os.path.exists( BUTTON_TEMP_FILE ) == False : return ""
    file = open( BUTTON_TEMP_FILE, "r" )
    irKeyName = file.read().strip()
    file.close()
    os.remove ( BUTTON_TEMP_FILE )
    print( "guzik: " + irKeyName )    
    return irKeyName
#-------------------------------------------------------------------------------------
def countAllMp3():
    return int(subprocess.run( [ myFolder() + "/cntmp3.sh" ], stdout=subprocess.PIPE ).stdout.decode('utf-8').splitlines()[0])
#-------------------------------------------------------------------------------------
def initPlaylists():
    global availablePlaylists
    global currentPlaylistIdx    
    global titlesTotal
    currentPlaylistIdx = 0
    availablePlaylists = []
    lcd.cursor_pos = (0, 0)
    lcd.write_string( fit20("inicjalizacja                     ") )        
    # stare precz!
    subprocess.run( ['rm', '*.m3u'] )        
    # odzyskaj liste dla radio
    subprocess.run( ['cp', '/home/pi/playlists/radio.m3u.org', '/home/pi/playlists/000_radio.m3u'] )    
    availablePlaylists.append( "000_radio" )    
    # iteracja po folderach na SDD i odbudowa list: jeden folder -> jedna playlista
    for mp3folder in sorted( os.listdir( SDD_STORAGE ) ):
#        print( mp3folder )
        lcd.cursor_pos = (1, 0)    
        lcd.write_string( fit20( mp3folder ) )    
        # dla każdego foldera - lista mp3 w pliku m3u, nazwa bez białych znaków
        playListFile = open( "/home/pi/playlists/" + mp3folder + ".m3u", "w" )         
        folderFullPath = "/mnt/usb_hdd_1/MP3/" + mp3folder
        for mp3File in sorted( os.listdir( folderFullPath ) ):
            mp3FullPath = folderFullPath + "/" + mp3File 
            playListFile.write( mp3FullPath + "\r\n" )            
#            print ( mp3FullPath )
        playListFile.close()
        # dodaj do splisu
        availablePlaylists.append( mp3folder )
    titlesTotal = countAllMp3()        
#-------------------------------------------------------------------------------------
def withZero( n ):
    return ( "000" + str( n ) )[-3:]
#-------------------------------------------------------------------------------------
def cleanStatusLine( s ):
    return s.replace("[playing]", "").replace("#", "").replace("\t", " ").replace("  ", " ").replace("(","").replace(")","").strip()
#-------------------------------------------------------------------------------------    
def setupMPC():
    subprocess.run( ['mpc', 'stop' ] )
    subprocess.run( ['mpc', 'volume',   '90'] )
    subprocess.run( ['mpc', 'repeat',   'on' ] )
    subprocess.run( ['mpc', 'random',   'off'] )   
    subprocess.run( ['mpc', 'single',   'off'] )   
#-------------------------------------------------------------------------------------
def playSelectedPlayList( idx ):
    plname = availablePlaylists[ idx ]
    lcd.cursor_pos = (0, 0)  #12345678901234567890
    lcd.write_string( fit20( "lista odtwarzania:  ") )
    lcd.cursor_pos = (1, 0)
    lcd.write_string( fit20( plname ) )   
    time.sleep( 1 )             
    subprocess.run( ['mpc', 'stop'] )
    subprocess.run( ['mpc', 'clear'] )
    subprocess.run( ['mpc', 'load', plname ] )
    subprocess.run( ['mpc', 'play', '1' ] )    
#-------------------------------------------------------------------------------------    
#def getIdleScreenLine( n ):
#    if n == 0: #12345678901234567890
#        return "NAS z e-Radio TT2020"
#    if n == 1:
#        return withZero( currentPlaylistIdx ) + "/" + withZero( len( availablePlaylists ) ) + " plikow:" + str(titlesTotal)
#    if n == 2:
#        dsi = subprocess.run( ["df","-h", SDD_STORAGE ,"--output=size,used,avail"], stdout=subprocess.PIPE ).stdout.decode('utf-8').splitlines()[1]
#        sizes = dsi.replace("   ", " ").replace("  ", " ").split(" ",3)                
#        return "wolne: " + sizes[3].replace("G","")+ " z "+ sizes[1].replace( "G","" ) + " GB"
#    if n == 3:
#        return "ip: " + getCurrentIp()
def getIdleScreenLine( n ):
    if n == 0 or n == 1: #12345678901234567890
        return "NAS z e-Radio TT2020"
    if n == 2 or n == 3:
        dsi = subprocess.run( ["df","-h", SDD_STORAGE ,"--output=size,used,avail"], stdout=subprocess.PIPE ).stdout.decode('utf-8').splitlines()[1]
        sizes = dsi.replace("   ", " ").replace("  ", " ").split(" ",3)                
        return str( len( availablePlaylists ) ) + "/" + str(titlesTotal) + "  " + sizes[2].replace("G","")+ "/"+ sizes[1].replace( "G","" ) + "GB"
#-------------------------------------------------------------------------------------
def fit20( s ):
    return ( s + "                    " )[:20]
#-------------------------------------------------------------------------------------                
def initLCD():
    return CharLCD( cols = 20, rows = 2, pin_rs = 26, pin_e=24, pins_data=[16, 18, 22, 8], numbering_mode=GPIO.BOARD )
#-------------------------------------------------------------------------------------                
def queryShutDown():
    bar = "####################"
    lastKey = ""
    while len(bar) > 0:
        lcd.cursor_pos = (0, 0)  #12345678901234567890
        lcd.write_string( fit20( "przycisk STOP zamyka") )
        lcd.cursor_pos = (1, 0)
        lcd.write_string( fit20( bar ) )
        bar = bar[0:len(bar)-1]
        currentKey = checkIrButtons()    
        if currentKey != "":
            lastKey = currentKey 
            if lastKey == "STOP": return True        
        time.sleep( 0.25 )         
    return False
#-------------------------------------------------------------------------------------                
def shutDownRadio():
    lcd.cursor_pos = (0, 0)
    lcd.write_string( fit20( "poczekaj chwile na  " ) )
    lcd.cursor_pos = (1, 0)
    lcd.write_string( fit20( "calkowite wylaczenie" ) )
    print( "shutdown here" )
    subprocess.run( ['shutdown', 'now'] )                                   
    while True: 
        pass
    return
#-------------------------------------------------------------------------------------                
# main
GPIO.setwarnings( False ) 
lcd = initLCD()
lastSecond = 0
lastKey = ""
availablePlaylists = []
currentPlaylistIdx = 0;
lastTitle = ""
scrollPosition = 0
infoCntr = 0
titlesTotal = 0

setupMPC()
initPlaylists()

while True:               
    time.sleep( 0.1 ) 
    currentKey = checkIrButtons()    
    if currentKey != "":
        lastKey = currentKey         
        if lastKey == "STOP":
            subprocess.run( ['mpc', 'stop'] )           
            
        if lastKey == "START":
            subprocess.run( ['mpc', 'play'] )           
            
        if lastKey == "BTN_0":  # czyli `RESET` na panelu
            currentPlaylistIdx = 0
            playSelectedPlayList( currentPlaylistIdx )
            
        if lastKey == "PLAY":  
            playSelectedPlayList( currentPlaylistIdx )
            
        if lastKey == "SEARCHPREV":
            subprocess.run( ['mpc', 'prev'] )                               

        if lastKey == "SEARCHNEXT":
            subprocess.run( ['mpc', 'next'] )                               
            
        if lastKey == "SKIPPREV":
            currentPlaylistIdx = currentPlaylistIdx - 1
            if currentPlaylistIdx < 0: currentPlaylistIdx = len( availablePlaylists ) -1
            playSelectedPlayList( currentPlaylistIdx )
            
        if lastKey == "SKIPNEXT":
            currentPlaylistIdx = currentPlaylistIdx + 1
            if currentPlaylistIdx > len( availablePlaylists ): currentPlaylistIdx = 0
            playSelectedPlayList( currentPlaylistIdx )
            
        if lastKey == "STANDBY":
            if queryShutDown() == True:
                shutDownRadio()
            else:
                # przeładuj wyświetlacz i listy
                setupMPC()
                initPlaylists()
                lcd = initLCD()
                
    now = datetime.now()    
    if lastSecond != now.second: 
        lastSecond = now.second   
        # zbadaj stan mpc (wersja na piechotę)
        mpcResult = subprocess.run( ['mpc'], stdout = subprocess.PIPE )
        mpcStdOut = mpcResult.stdout.decode('utf-8')
        mpcLines = mpcStdOut.splitlines()    
        if len( mpcLines) == 3: 
            # tu gra
            if lastTitle != mpcLines[0]:
                lastTitle = mpcLines[0]
                scrollPosition = 0            
            lcd.cursor_pos = (0, 0)
            lastTitleTrimmed = lastTitle.replace( SDD_STORAGE ,"").replace(".mp3","").replace("/", " ")
            lcd.write_string( fit20( ( lastTitleTrimmed + " * " + lastTitleTrimmed + " * ")[scrollPosition:] ) )            
            scrollPosition = scrollPosition + 1
            if scrollPosition > len( lastTitle ):
                scrollPosition = 0            
            lcd.cursor_pos = (1, 0)
            lcd.write_string( fit20( cleanStatusLine( mpcLines[1] ) ) )
        else:
            # tu nie gra
            lcd.cursor_pos = (0, 0)
            lcd.write_string( fit20 ( getIdleScreenLine ( infoCntr % 4 ) ) )        
            if lastSecond % 3 == 0: infoCntr = infoCntr + 1
            lcd.cursor_pos = (1, 0)    
            lcd.write_string( fit20( "      " + now.strftime("%H:%M:%S") ) )    
    lastKey = ""

# fin

