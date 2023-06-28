############ to drive motor to initial angle#######################
import RPi.GPIO as GPIO
import time
import numpy as np

#define gpio pin for servo
servo_pin_verti = 17
#duty -> to caculate motor angle (pwm)
SERVO_MAX_DUTY = 12
SERVO_MIN_DUTY = 3
#set servo mode and allocate pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin_verti, GPIO.OUT)
#make servo instance and adjust it as '0' angle
servo_verti = GPIO.PWM(servo_pin_verti, 50)
servo_verti.start(0)
#chage duty to angle
def servo_control_verti(degree,delay):
    if degree > 180:
        degree = 180
    
    duty = SERVO_MIN_DUTY + (degree * (SERVO_MAX_DUTY - SERVO_MIN_DUTY) / 180.0)
    #print("Degree: {} to {}(Duty)".format(degree,duty))
    servo_verti.ChangeDutyCycle(duty)
    time.sleep(delay)
servo_control_verti(130,0.5)
servo_verti.stop()
GPIO.cleanup()
#################################################################################

import time
import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219

import pymysql
import time

db = None
cur = None

db = pymysql.connect(host = '219.241.123.226', port = 10122, user = 'inventist', password = 'bems', db = 'mysql', charset = 'utf8')


i2c_bus = board.I2C()

ina219 = INA219(i2c_bus)

print("ina219 test")

# display some of the advanced field (just to test)
print("Config register:")
print("  bus_voltage_range:    0x%1X" % ina219.bus_voltage_range)
print("  gain:                 0x%1X" % ina219.gain)
print("  bus_adc_resolution:   0x%1X" % ina219.bus_adc_resolution)
print("  shunt_adc_resolution: 0x%1X" % ina219.shunt_adc_resolution)
print("  mode:                 0x%1X" % ina219.mode)
print("")

# optional : change configuration to use 32 samples averaging for both bus voltage and shunt voltage
ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
# optional : change voltage range to 16V
ina219.bus_voltage_range = BusVoltageRange.RANGE_16V

# measure and display loop
power_sum = []
while True:
    
    bus_voltage = ina219.bus_voltage  # voltage on V- (load side)
    shunt_voltage = ina219.shunt_voltage  # voltage between V+ and V- across the shunt
    current = ina219.current  # current in mA
    power = ina219.power  # power in watts

    # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage
    #print("Voltage (VIN+) : {:6.3f}   V".format(bus_voltage + shunt_voltage))
    #print("Voltage (VIN-) : {:6.3f}   V".format(bus_voltage))
    #print("Shunt Voltage  : {:8.5f} V".format(shunt_voltage))
    #print("Shunt Current  : {:7.4f}  A".format(current / 1000))
    print("Power Calc.    : {:8.5f} W".format(bus_voltage * (current / 1000) + 0.00101))
    #print("Power Register : {:6.3f}   W".format(power))
    print("")
    
    power_sum.append(bus_voltage * (current / 1000) + 0.00101)
    
    if len(power_sum) == 10:
        Power = sum(power_sum)/10
        db = pymysql.connect(host = '219.241.123.226', port = 10122, user = 'inventist', password = 'bems', db = 'mysql', charset = 'utf8')
        cur = db.cursor()
        cur.execute('INSERT INTO BEMS(panel_charge) VALUES ({})'.format(Power))
        db.commit()

        print("10th_power_sum :", Power)
        power_sum = []
    
    # Check internal calculations haven't overflowed (doesn't detect ADC overflows)
    if ina219.overflow:
        print("Internal Math Overflow Detected!")
        print("")

    time.sleep(1)
    