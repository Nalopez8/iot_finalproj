import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from time import sleep
import os
GPIO.setwarnings(False)

reader = SimpleMFRC522()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(38,GPIO.OUT)
pwm=GPIO.PWM(38,50)

def SetAngle(angle):
    duty=angle/18+2
    GPIO.output(38,True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(38,False)
    pwm.ChangeDutyCycle(0)



text = input("Enter Name: ")
print("Place tag to enter")

try:
    reader.write(text)
    print("Written")
   
    pwm.start(0)
    SetAngle(90)
    sleep(2)
    SetAngle(0)
   

   
    print("place tag to exit\n")
    id,text = reader.read()
    print(id)
    print("Have a nice day!")
    print(text)
   
   
    SetAngle(90)
    sleep(2)
    SetAngle(0)
    pwm.stop()
   
finally:
    GPIO.cleanup()
   
sleep(1)

######Just be sure to change the directory below to the proper directory where the zip file will be extracted
os.system('python3 /home/pi/Downloads/iot_finalproj-main/lcd_sens.py')
