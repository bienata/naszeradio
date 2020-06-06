from datetime import datetime
from RPLCD import CharLCD
import RPi.GPIO as GPIO
from pathlib import Path
import subprocess
import time
import os
import biglcd

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
def getIdleScreenLine( n ):
    if n == 0 or n == 1: #12345678901234567890
        return "NAS z e-Radio TT2020"
    if n == 2 or n == 3:
        dsi = subprocess.run( ["df","-h", SDD_STORAGE ,"--output=size,used,avail"], stdout=subprocess.PIPE ).stdout.decode('utf-8').splitlines()[1]
        sizes = dsi.replace("   ", " ").replace("  ", " ").split(" ",3)                
        return str( len( availablePlaylists ) ) + "/" + str(titlesTotal) + "  " + sizes[2].replace("G","")+ "/"+ sizes[1].replace( "G","" ) + "GB"
#-------------------------------------------------------------------------------------
def fit20( s ):
    return ( s + "                    " )[:24]
#-------------------------------------------------------------------------------------                
def initLCD():
    lcd = CharLCD( cols = 24, rows = 2, pin_rs = 26, pin_e=24, pins_data=[16, 18, 22, 8], numbering_mode=GPIO.BOARD )
    biglcd.createLcdCustomChar( lcd )
    return lcd
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
def showIdleClock( s ):
    lcd.cursor_pos = (0, 0)    
    lcd.write_string( "   " )
    lcd.cursor_pos = (1, 0)    
    lcd.write_string( "   " )
    lcd.cursor_pos = (0, 6)    
    lcd.write_string( " " )
    lcd.cursor_pos = (1, 6)    
    lcd.write_string( " " )
    lcd.cursor_pos = (0, 16)    
    lcd.write_string( " " )
    lcd.cursor_pos = (1, 16)    
    lcd.write_string( " " )

    t = now.strftime("%H%M%S")   # 0123ss
    # 012345678901234567890123
    # .  .  .  .  .  .  .  .    
    biglcd.write(lcd, 3, t[0:1] )
    biglcd.write(lcd, 7, t[1:2] )
    if s % 2 == 0:
        biglcd.write(lcd, 10, ':' )
    else:
        biglcd.write(lcd, 10, ' ' )        
    biglcd.write(lcd, 13, t[2:3] )
    biglcd.write(lcd, 17, t[3:4] )
    lcd.cursor_pos = (0, 20)    
    lcd.write_string( "      " )
    lcd.cursor_pos = (1, 20)    
    lcd.write_string( " :" + t[4:] )        

def showIdleInfo( lastSecond ):
    lcd.cursor_pos = (0, 0)
    dsi = subprocess.run( ["df","-h", SDD_STORAGE ,"--output=size,used,avail"], stdout=subprocess.PIPE ).stdout.decode('utf-8').splitlines()[1]
    sizes = dsi.replace("   ", " ").replace("  ", " ").split(" ",3)                
    lcd.write_string( fit20( "T:" + str(titlesTotal) + " A:" + str( len( availablePlaylists ) ) + " Z:" + sizes[2].replace("G","")+ "/" + sizes[1].replace( "G","" ) + "G       " ) )    
    lcd.cursor_pos = (1, 0)    
    lcd.write_string( fit20( now.strftime("%H:%M:%S") + " IP:" + getCurrentIp() ) )    

def showNumQueue( q ):    
    # 012345678901234567890123
    # xxxyyyqqq   PLAY zaczyna        
    biglcd.write(lcd, 0, q[0:1] )
    biglcd.write(lcd, 3, q[1:2] )
    biglcd.write(lcd, 6, q[2:3] )
    biglcd.write(lcd, 9, ' ' )
    lcd.cursor_pos = (0, 12)
    lcd.write_string( "            "  )        
    lcd.cursor_pos = (1, 12)
    lcd.write_string( "            " )        
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
idleScreenMode=True
numQueue="___"
lastNumQueue="___"
numQcntr=0

setupMPC()
initPlaylists()

while True:               
    time.sleep( 0.1 ) 
    currentKey = checkIrButtons()    
    if currentKey != "":
        lastKey = currentKey    

        if lastKey == "BTN_0":
            numQueue += "0"
        if lastKey == "BTN_1":
            numQueue += "1"
        if lastKey == "BTN_2":
            numQueue += "2"
        if lastKey == "BTN_3":
            numQueue += "3"
        if lastKey == "BTN_4":
            numQueue += "4"
        if lastKey == "BTN_5":
            numQueue += "5"
        if lastKey == "BTN_6":
            numQueue += "6"
        if lastKey == "BTN_7":
            numQueue += "7"
        if lastKey == "BTN_8":
            numQueue += "8"
        if lastKey == "BTN_9":
            numQueue += "9"

        if lastKey == "TITR":
            idleScreenMode ^= True
        
        if lastKey == "STOP":
            subprocess.run( ['mpc', 'stop'] )           
            
        if lastKey == "START":
            subprocess.run( ['mpc', 'play'] )           
                        
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
    #
    now = datetime.now()    
    
    if lastNumQueue != numQueue:        
        numQueue = numQueue[-3:]
        lastNumQueue = numQueue
        numQcntr=70
        showNumQueue( numQueue )

    if numQcntr > 0:
        numQcntr -= 1        
        if numQcntr < 10:
            if numQcntr % 2 == 0:
                showNumQueue( numQueue )
            else:
                showNumQueue( '___' )
        if numQcntr <= 0:
            toSearch = ("000" + numQueue.replace("_",""))[-3:]
            for i in range (0, len( availablePlaylists )):
                if availablePlaylists[i][:3] == toSearch: 
                    print(availablePlaylists[i])
                    currentPlaylistIdx = i
                    break                
            playSelectedPlayList( currentPlaylistIdx )            
            numQueue="___"
            lastNumQueue="___"            
        
    if lastSecond != now.second and numQueue == "___": 
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
            if idleScreenMode == True:
                showIdleClock( lastSecond )
            else:
                showIdleInfo( lastSecond )
            #fi
        #fi
    #fi
    lastKey = ""    

# fin

