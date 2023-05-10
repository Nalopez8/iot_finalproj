import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from time import sleep
import os
GPIO.setwarnings(False)

##########Call libraries for RFID Simple MFRC522


########Define the reader and the pin for servo motor
reader = SimpleMFRC522()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(38,GPIO.OUT)

############50 represents  frequency of 50Hz
pwm=GPIO.PWM(38,50)

#####Function to convert entered angle to required duty cycles for servo motor
def SetAngle(angle):
    duty=angle/18+2
    GPIO.output(38,True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(38,False)
    pwm.ChangeDutyCycle(0)


######Prompts user to enter their name and to bring tag near reader
text = input("Enter Name: ")
print("Place tag to enter")

try:
    ####Once tag is brought near, name is written to RFID module
    reader.write(text)
    print("Written")
   

    ######Use Angle function to open gate and close after 2 seconds
    pwm.start(0)
    SetAngle(90)
    sleep(2)
    SetAngle(0)
   

   ######Wait for tag to be brought near reader again
    print("place tag to exit\n")
    id,text = reader.read()
    
    #####Print tag ID and name, along with message
    print(id)
    print("Have a nice day!")
    print(text)
   
   ####Open and close gate again 
    SetAngle(90)
    sleep(2)
    SetAngle(0)
    pwm.stop()
   
finally:
    GPIO.cleanup()
   
sleep(1)

######Just be sure to change the directory below to the proper directory where the zip file will be extracted
##### should be something like /home/pi/specific_folder_saved_in/lcd_sens.py
#### This opens the other set of code and runs the count/sensor check
os.system('python3 /home/pi/Downloads/iot_finalproj-main/lcd_sens.py')
