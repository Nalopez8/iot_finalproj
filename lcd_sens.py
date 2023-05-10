#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os,sys
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

'''
define pin for lcd
'''
# Timing constants for LCD Display
E_PULSE = 0.0005
E_DELAY = 0.0005
delay = 1


                       
# Define GPIO to LCD mapping
# RS is read, E is enable, D4-D7 are data pins
LCD_RS = 7                                                                                                                                                                                                              
LCD_E  = 11
LCD_D4 = 12
LCD_D5 = 13
LCD_D6 = 15
LCD_D7 = 16

###Define pins for IR sensors
slot1_Sensor = 29
slot2_Sensor = 31

###Set LCD Pins as output and IR Sensor Pins as Input
GPIO.setup(LCD_E, GPIO.OUT)  # E
GPIO.setup(LCD_RS, GPIO.OUT) # RS
GPIO.setup(LCD_D4, GPIO.OUT) # DB4
GPIO.setup(LCD_D5, GPIO.OUT) # DB5
GPIO.setup(LCD_D6, GPIO.OUT) # DB6
GPIO.setup(LCD_D7, GPIO.OUT) # DB7
GPIO.setup(slot1_Sensor, GPIO.IN)
GPIO.setup(slot2_Sensor, GPIO.IN)

# Define  device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True  ### character
LCD_CMD = False   #####command
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

'''
Function Name :lcd_init()
Function Description : this function is used to initialized lcd by sending the different commands
'''
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)
'''
Function Name :lcd_byte(bits ,mode)
Fuction Name :the main purpose of this function to convert the byte data into bit and send to lcd port
'''
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
  #### number for bits depends on what would like to be done like clear, iniitialise, etc. 
 
  GPIO.output(LCD_RS, mode) # RS
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
'''
Function Name : lcd_toggle_enable()
Function Description: This is used to toggle Enable pin
'''
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
'''
Function Name :lcd_string(message,line)
Function  Description :print the data on lcd
The Message goes in double quotes " ", other field
specifies the line we would like to display on

'''

   
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    ####Prints characters from message to display
    lcd_byte(ord(message[i]),LCD_CHR)
   
  ####Function to display "Full" when the count is 0
def count0():
    lcd_string("Full           ",LCD_LINE_1)
    time.sleep(0.5)
    lcd_byte(0x01,LCD_CMD)

 
  #####Function to display "1 Space Open" when the count is 1
def count1():
    lcd_string("1 Space(s) Open",LCD_LINE_1)
    time.sleep(0.5)
    lcd_byte(0x01,LCD_CMD)
   
   #####Function to display "1 Space Open" when the count is 2
def count2():
    lcd_string("2 Space(s) Open",LCD_LINE_1)
    time.sleep(0.5)
    lcd_byte(0x01,LCD_CMD)
    
    
###Function used in testing to see if count could be held
def lcd_count(count,line):
  # Send string to display
 
  count= count.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
      lcd_byte(ord(count[i]),LCD_CHR)

####Initialize display, display welcome message, clear
lcd_init()
lcd_string("Welcome to",LCD_LINE_1)
time.sleep(0.5)
lcd_string("Car Parking ",LCD_LINE_1)
lcd_string("System ",LCD_LINE_2)
time.sleep(0.5)
lcd_byte(0x01,LCD_CMD) # 000001 Clear display
# Define delay between readings
#lcd_string("Slots Open",LCD_LINE_1)
delay = 5


##############Function to check the spots available and to determine count 
def check_spots(slot1_status,slot2_status):
  #########This is the condition if both spots are available (Count is 2)
    if((slot1_status == True) and (slot2_status==True)):
        count=2
        time.sleep(0.2)
        count2()
        lcd_byte(0x01,LCD_CMD)
        delay=5


#########This is the condition if one spot is available (Count is 1)
    if((slot1_status == True) and (slot2_status==False)):
        count=1
        time.sleep(0.2)
        count1()
        lcd_byte(0x01,LCD_CMD)
        delay=5
       

#########This is the condition if one spot is available (Count is 1)
    if((slot1_status == False) and (slot2_status==True)):
        count=1
        time.sleep(0.2)
        count1()
        lcd_byte(0x01,LCD_CMD)
        delay=5

#########This is the condition if there are no spots available (Count is 0)
    if((slot1_status == False) and (slot2_status==False)):
        count=0
        time.sleep(0.2)
        count0()
        lcd_byte(0x01,LCD_CMD)
        delay=5

##########Prints the amount of spots available to Python Shell
    print("Slots Open:",count)
   

while 1:
   
    #####Check the sensor status and clear display every 0.1 seconds
    slot1_status = GPIO.input(slot1_Sensor)
    time.sleep(0.1)
    slot2_status = GPIO.input(slot2_Sensor)
    time.sleep(0.1)
    check_spots(slot1_status,slot2_status)
    time.sleep(0.1)
    lcd_byte(0x01,LCD_CMD)
    delay =5
