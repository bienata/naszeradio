# obsluga wielkich znakow w semigrafice
semi0 = (
    0b00111,
    0b01111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111
)
semi1 = (
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b01111,
    0b00111
)
semi2 = (
    0b11111,
    0b11111,
    0b11111,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000
)
semi3 = (
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b11111,
    0b11111,
    0b11111
)
semi4 = (
    0b11100,
    0b11110,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111
)
semi5 = (
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11110,
    0b11100
)

semi6 = (
    0b11111,
    0b11111,
    0b11111,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b11111
)

semi7 = (
    0b11111,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b11111,
    0b11111,
    0b11111
)

def createLcdCustomChar( lcd ):
    lcd.create_char( 0x00, semi0 )
    lcd.create_char( 0x01, semi1 )
    lcd.create_char( 0x02, semi2 )
    lcd.create_char( 0x03, semi3 )
    lcd.create_char( 0x04, semi4 )
    lcd.create_char( 0x05, semi5 )
    lcd.create_char( 0x06, semi6 )
    lcd.create_char( 0x07, semi7 )

def write0(lcd, n ):
    lcd.cursor_pos = (0, n)
    lcd.write_string( str( chr(0x00) ) )
    lcd.write_string( str( chr(0x02) ) )
    lcd.write_string( str( chr(0x04) ) )    
    lcd.cursor_pos = (1, n)
    lcd.write_string( str( chr(0x01) ) )
    lcd.write_string( str( chr(0x03) ) )
    lcd.write_string( str( chr(0x05) ) )    
    return

def write1(lcd, n ):
    lcd.cursor_pos = (0, n)
    lcd.write_string( ' ' )
    lcd.write_string( str( chr(0x04) ) )
    lcd.write_string( ' ' )    
    lcd.cursor_pos = (1, n)
    lcd.write_string( ' ' )
    lcd.write_string( str( chr(0x01) ) )
    lcd.write_string( ' ' )    

def write2(lcd, n ):
    lcd.cursor_pos = (0, n)
    lcd.write_string( str( chr(0x02) ) )
    lcd.write_string( str( chr(0x06) ) )
    lcd.write_string( str( chr(0x04) ) )
    lcd.cursor_pos = (1, n)
    lcd.write_string( str( chr(0x01) ) )
    lcd.write_string( str( chr(0x07) ) )
    lcd.write_string( str( chr(0x03) ) )    

def write3(lcd, n ):
    lcd.cursor_pos = (0, n)
    lcd.write_string( str( chr(0x02) ) )
    lcd.write_string( str( chr(0x06) ) )
    lcd.write_string( str( chr(0x04) ) )    
    lcd.cursor_pos = (1, n)
    lcd.write_string( str( chr(0x03) ) )
    lcd.write_string( str( chr(0x07) ) )
    lcd.write_string( str( chr(0x05) ) )    

def write4(lcd, n ):
    lcd.cursor_pos = (0, n)
    lcd.write_string( str( chr(0x01) ) )
    lcd.write_string( str( chr(0x03) ) )
    lcd.write_string( str( chr(0x04) ) )    
    lcd.cursor_pos = (1, n)
    lcd.write_string( ' ' )
    lcd.write_string( ' ' )
    lcd.write_string( str( chr(0x05) ) )    

def write5(lcd, n ):
    lcd.cursor_pos = (0, n)
    lcd.write_string( str( chr(0x00) ) )
    lcd.write_string( str( chr(0x06) ) )
    lcd.write_string( str( chr(0x06) ) )    
    lcd.cursor_pos = (1, n)
    lcd.write_string( str( chr(0x07) ) )
    lcd.write_string( str( chr(0x07) ) )
    lcd.write_string( str( chr(0x05) ) )    

def write6(lcd, n ):
    lcd.cursor_pos = (0, n)
    lcd.write_string( str( chr(0x00) ) )
    lcd.write_string( str( chr(0x06) ) )
    lcd.write_string( str( chr(0x02) ) )    
    lcd.cursor_pos = (1, n)
    lcd.write_string( str( chr(0x01) ) )
    lcd.write_string( str( chr(0x03) ) )
    lcd.write_string( str( chr(0x05) ) )

def write7(lcd, n ):
    lcd.cursor_pos = (0, n)
    lcd.write_string( str( chr(0x02) ) )
    lcd.write_string( str( chr(0x02) ) )
    lcd.write_string( str( chr(0x04) ) )    
    lcd.cursor_pos = (1, n)
    lcd.write_string( ' ' )
    lcd.write_string( ' ' )
    lcd.write_string( str( chr(0x05) ) )

def write8(lcd, n ):
    lcd.cursor_pos = (0, n)
    lcd.write_string( str( chr(0x00) ) )
    lcd.write_string( str( chr(0x06) ) )
    lcd.write_string( str( chr(0x04) ) )
    lcd.cursor_pos = (1, n)
    lcd.write_string( str( chr(0x01) ) )
    lcd.write_string( str( chr(0x07) ) )
    lcd.write_string( str( chr(0x05) ) )

def write9(lcd, n ):
    lcd.cursor_pos = (0, n)
    lcd.write_string( str( chr(0x00) ) )
    lcd.write_string( str( chr(0x06) ) )
    lcd.write_string( str( chr(0x04) ) )    
    lcd.cursor_pos = (1, n)
    lcd.write_string( str( chr(0x03) ) )
    lcd.write_string( str( chr(0x07) ) )
    lcd.write_string( str( chr(0x05) ) )

def writeColon(lcd, n ):
    lcd.cursor_pos = (0, n)
    lcd.write_string( ' ' )
    lcd.write_string( 'o' )
    lcd.write_string( ' ' )    
    lcd.cursor_pos = (1, n)
    lcd.write_string( ' ' )
    lcd.write_string( 'o' )
    lcd.write_string( ' ' )    

def writeFloor(lcd, n ):
    lcd.cursor_pos = (0, n)
    lcd.write_string( ' ' )
    lcd.write_string( ' ' )
    lcd.write_string( ' ' )    
    lcd.cursor_pos = (1, n)
    lcd.write_string( '_' )
    lcd.write_string( '_' )
    lcd.write_string( '_' )    

def writeSpace(lcd, n ):
    lcd.cursor_pos = (0, n)
    lcd.write_string( ' ' )
    lcd.write_string( ' ' )
    lcd.write_string( ' ' )    
    lcd.cursor_pos = (1, n)
    lcd.write_string( ' ' )
    lcd.write_string( ' ' )
    lcd.write_string( ' ' )    

def write(lcd, n, s):
    charMap = { '0': write0, '1' : write1, '2' : write2, '3' : write3, '4' : write4, '5': write5, '6' : write6, '7' : write7, '8' : write8, '9' : write9, ':' : writeColon, '_' : writeFloor, ' ' : writeSpace }    
    charMap[ s ](lcd, n)

#fin
