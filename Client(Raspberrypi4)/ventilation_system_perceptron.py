#exchage = 1, bypass = 0
import numpy as np

#temp_in, out have to be taken by sql or app !
##################
temp_in = int(input('indoor temperature : '))
temp_out = int(input('Outdoor temperature : '))
hud_in = int(input('indoor hudmidity : '))
hud_out = int(input('Outdoor hudmidity : '))
##################

#make input data (out - in)
temp = temp_out - temp_in
hud = hud_out - hud_in

#input data (out - in), this will be the input data of perceptron
tempnhud= np.array([temp,hud]) 

def perceptron(x,season):
    x_1 = x[0]
    x_2 = x[1]
    
    if season == 'spring':
        perceptron_fall = -5.99 * x_1 + 7.3 * x_2 - 7.799
        if perceptron_fall > 0:
            system = 'heat exchage'
        else:
            system = 'bypass'
            
    if season == 'summer':
        perceptron_fall = 10 * x_1 + 4.6 * x_2 + 15
        if perceptron_fall > 0:
            system = 'heat exchage'
        else:
            system = 'bypass'
            
    if season == 'fall':
        perceptron_fall = -14.3 * x_1 + 8.5 * x_2 - 0.599
        if perceptron_fall > 0:
            system = 'heat exchage'
        else:
            system = 'bypass'
            
    if season == 'winter':
        perceptron_fall = -28.67 * x_1 + 19.3 * x_2 - 0.599
        if perceptron_fall > 0:
            system = 'heat exchage'
        else:
            system = 'bypass'
    
    return system

system = perceptron(tempnhud,'winter')
print('System is :',system)

import RPi.GPIO as GPIO
import time
import numpy as np

#define led pin num
LED_R = 17
LED_G = 27
#define gpio pin for servo
servo_pin_damper1 = 2
servo_pin_damper2 = 3

#duty -> to caculate motor angle (pwm)
SERVO_MAX_DUTY = 12
SERVO_MIN_DUTY = 3

#set servo mode and allocate pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_R,GPIO.OUT)
GPIO.setup(LED_G,GPIO.OUT)
GPIO.setup(servo_pin_damper1, GPIO.OUT)
GPIO.setup(servo_pin_damper2,GPIO.OUT)

LED_R_heatexchange = GPIO.PWM(LED_R,500)
LED_G_heatexchange = GPIO.PWM(LED_G,500)

#make servo instance and adjust it as '0' angle
servo_damper1 = GPIO.PWM(servo_pin_damper1, 50)
servo_damper2 = GPIO.PWM(servo_pin_damper2, 50)
servo_damper1.start(0)
servo_damper2.start(0)

if system == "bypass":
    angle = 0
    duty = 3.0
    
    LED_R_heatexchange.start(100)
    LED_R_heatexchange.ChangeDutyCycle(100)
    
else:
    angle = 180
    duty = 12
    
    LED_G_heatexchange.start(100)
    LED_G_heatexchange.ChangeDutyCycle(100)


servo_damper1.ChangeDutyCycle(duty)
time.sleep(1)
servo_damper1.stop()
servo_damper2.ChangeDutyCycle(duty)
time.sleep(1)
servo_damper2.stop()

time.sleep(3)


LED_G_heatexchange.stop()
LED_R_heatexchange.stop()
GPIO.cleanup()
 