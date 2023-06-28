#-*- coding:utf-8 -*-

############## to get API#################
import requests
import requests
import pprint
from os import name
import xml.etree.ElementTree as et
import pandas as pd
import bs4
from lxml import html
from urllib.parse import urlencode, quote_plus, unquote
############ to drive motor#######################
import RPi.GPIO as GPIO
import time
import numpy as np
############# to make panel downward with thread ###################
import threading
import time
################# database ####################
import spidev
import pymysql
import time
#############################################

########################API##################################
def interpolate_alt(df, alt9,alt12,alt15,alt18):
    interpolate_morning = (alt12 - alt9) / 3
    df.insert(loc = 0, column = 'altitude_06', value = alt9 - 3 * interpolate_morning + 90,allow_duplicates=True)
    df.insert(loc = 0,column = 'altitude_07', value = alt9 - 2 * interpolate_morning+ 90,allow_duplicates=True)
    df.insert(loc = 0,column = 'altitude_08', value = alt9 - 1 * interpolate_morning+ 90,allow_duplicates=True)
    df.insert(loc = 0,column = 'altitude_09', value = alt9 - 0 * interpolate_morning+ 90,allow_duplicates=True)
    df.insert(loc = 0,column = 'altitude_10', value = alt9 + 1 * interpolate_morning+ 90,allow_duplicates=True)
    df.insert(loc = 0,column = 'altitude_11', value = alt9 + 2 * interpolate_morning+ 90,allow_duplicates=True)
    df.insert(loc = 0,column = 'altitude_12', value = alt9 + 3 * interpolate_morning+ 90,allow_duplicates=True)
    df.insert(loc = 0,column = 'altitude_13', value = alt9 + 4 * interpolate_morning+ 90,allow_duplicates=True)

    interpolate_afternoon = (alt15 - alt18) / 3
    df.insert(loc = 0,column = 'altitude_14', value = alt15 + 1 * interpolate_afternoon+ 90,allow_duplicates=True)
    df.insert(loc = 0,column = 'altitude_15', value = alt15 - 0 * interpolate_afternoon+ 90,allow_duplicates=True)
    df.insert(loc = 0,column = 'altitude_16', value = alt15 - 1 * interpolate_afternoon+ 90,allow_duplicates=True)
    df.insert(loc = 0,column = 'altitude_17', value = alt15 - 2 * interpolate_afternoon+ 90,allow_duplicates=True)
    df.insert(loc = 0,column = 'altitude_18', value = alt15 - 3 * interpolate_afternoon+ 90,allow_duplicates=True)

    return df

def interpolate_azi(df, azi9,azi12,azi15,azi18):
    interpolate_morning = (azi12 - azi9) / 3
    df.insert(loc = 0, column = 'azimuth_06', value = azi9 - 3 * interpolate_morning,allow_duplicates=True)
    df.insert(loc = 0,column = 'azimuth_07', value = azi9 - 2 * interpolate_morning,allow_duplicates=True)
    df.insert(loc = 0,column = 'azimuth_08', value = azi9 - 1 * interpolate_morning,allow_duplicates=True)
    df.insert(loc = 0,column = 'azimuth_09', value = azi9 - 0 * interpolate_morning,allow_duplicates=True)
    df.insert(loc = 0,column = 'azimuth_10', value = azi9 + 1 * interpolate_morning,allow_duplicates=True)
    df.insert(loc = 0,column = 'azimuth_11', value = azi9 + 2 * interpolate_morning,allow_duplicates=True)
    df.insert(loc = 0,column = 'azimuth_12', value = azi9 + 3 * interpolate_morning,allow_duplicates=True)
    
    interpolate_lunch = (azi15 - azi12) / 3
    df.insert(loc = 0,column = 'azimuth_13', value = azi12 + 1 * interpolate_lunch,allow_duplicates=True)
    df.insert(loc = 0,column = 'azimuth_14', value = azi12 + 2 * interpolate_lunch,allow_duplicates=True)
    df.insert(loc = 0,column = 'azimuth_15', value = azi12 + 3 * interpolate_lunch,allow_duplicates=True)

    
    interpolate_afternoon = (azi18 - azi15) / 3
    df.insert(loc = 0,column = 'azimuth_16', value = azi15 + 1 * interpolate_afternoon,allow_duplicates=True)
    df.insert(loc = 0,column = 'azimuth_17', value = azi15 + 2 * interpolate_afternoon,allow_duplicates=True)
    df.insert(loc = 0,column = 'azimuth_18', value = azi18 ,allow_duplicates=True)

    return df
    
def get_azinalt_interpolate(location,locdate):

    url = 'http://apis.data.go.kr/B090041/openapi/service/SrAltudeInfoService/getAreaSrAltudeInfo'
    params ={'serviceKey' : 'qvo6k/RRFBXFU33mRurNZeqkmgT4aKAOwx6TOFSVGnT6xUFLxqHpWgibBke+6jDY9P8HIzJZMwer+rUu3+xYIw==', 'location' : location, 'locdate' : locdate }

    response = requests.get(url, params=params)

    # xml 내용
    content = response.text

    # 깔끔한 출력 위한 코드
    pp = pprint.PrettyPrinter(indent=4)

    xml_obj = bs4.BeautifulSoup(content,'lxml-xml')
    rows = xml_obj.findAll('item')

    # 각 행의 컬럼, 이름, 값을 가지는 리스트 만들기
    row_list = [] # 행값
    name_list = [] # 열이름값
    value_list = [] #데이터값

    # xml 안의 데이터 수집
    for i in range(0, len(rows)):
        columns = rows[i].find_all()
        #첫째 행 데이터 수집
        for j in range(0,len(columns)):
            if i ==0:
                # 컬럼 이름 값 저장
                name_list.append(columns[j].name)
            # 컬럼의 각 데이터 값 저장
            value_list.append(columns[j].text)
        # 각 행의 value값 전체 저장
        row_list.append(value_list)
        # 데이터 리스트 값 초기화
        value_list=[]
    
    solar_df = pd.DataFrame(row_list, columns=name_list)
    alt_df = solar_df[['altitude_09','altitude_12','altitude_15','altitude_18']]
    azi_df = solar_df[['azimuth_09','azimuth_12','azimuth_15','azimuth_18']]
    
    alt9 = int(str(alt_df['altitude_09'])[5:7])
    alt12 = int(str(alt_df['altitude_12'])[5:7])
    alt15 = int(str(alt_df['altitude_15'])[5:7])
    alt18 = int(str(alt_df['altitude_18'])[5:7])
    
    alt_df_interpolate = pd.DataFrame(index=range(0,1), columns = ['altitude_06','altitude_07','altitude_08','altitude_09','altitude_10','altitude_11','altitude_12','altitude_13','altitude_14','altitude_15','altitude_16','altitude_17','altitude_18'])
    
    alt_df_interpolate = interpolate_alt(alt_df_interpolate,alt9,alt12,alt15,alt18).dropna(axis= 1)[['altitude_06','altitude_07','altitude_08','altitude_09','altitude_10','altitude_11','altitude_12','altitude_13','altitude_14','altitude_15','altitude_16','altitude_17','altitude_18']]
    
    azi9 = int(str(azi_df['azimuth_09'])[5:8])
    azi12 = int(str(azi_df['azimuth_12'])[5:8])
    azi15 = int(str(azi_df['azimuth_15'])[5:8])
    azi18 = int(str(azi_df['azimuth_18'])[5:8])
    
    azi_df_interpolate = pd.DataFrame(index=range(0,1), columns = ['azimuth_06','azimuth_07','azimuth_08','azimuth_09','azimuth_10','azimuth_11','azimuth_12','azimuth_13','azimuth_14','azimuth_15','azimuth_16','azimuth_17','azimuth_18'])

    azi_df_interpolate = interpolate_azi(azi_df_interpolate,azi9,azi12,azi15,azi18).dropna(axis= 1)[['azimuth_06','azimuth_07','azimuth_08','azimuth_09','azimuth_10','azimuth_11','azimuth_12','azimuth_13','azimuth_14','azimuth_15','azimuth_16','azimuth_17','azimuth_18']]
    
    return sum(alt_df_interpolate.values.tolist(),[]), sum(azi_df_interpolate.values.tolist(),[])

#############################################################################################

######################## drive motors with API #################################################

#define gpio pin for servo
servo_pin_verti = 12 #17
servo_pin_horiz = 13 #27

#duty -> to caculate motor angle (pwm)
SERVO_MAX_DUTY = 12
SERVO_MIN_DUTY = 3

#set servo mode and allocate pin
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(servo_pin_verti, GPIO.OUT)
#GPIO.setup(servo_pin_horiz,GPIO.OUT)

#make servo instance and adjust it as '0' angle
#servo_verti = GPIO.PWM(servo_pin_verti, 50)
#servo_horiz = GPIO.PWM(servo_pin_horiz, 50)
#servo_verti.start(0)
#servo_horiz.start(0)


#chage duty to angle
def servo_control_verti(degree,delay):   
    if degree > 180:
        degree = 180
        
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin_verti, GPIO.OUT)
    servo_verti = GPIO.PWM(servo_pin_verti, 50)
    servo_verti.start(0)
    
    duty = SERVO_MIN_DUTY + (degree * (SERVO_MAX_DUTY - SERVO_MIN_DUTY) / 180.0)
    #print('verti duty is :', duty)
    #print("Degree: {} to {}(Duty)".format(degree,duty))
    #GPIO.setup(servo_pin_verti, GPIO.OUT)
    servo_verti.ChangeDutyCycle(duty)
    time.sleep(delay)
    #GPIO.setup(servo_pin_verti, GPIO.IN)
    
    servo_verti.stop()
    GPIO.cleanup()
    
def servo_control_horiz(degree,delay):
    if degree > 180:
        degree = 180
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin_horiz, GPIO.OUT)
    servo_horiz = GPIO.PWM(servo_pin_horiz, 50)
    servo_horiz.start(0)
    
    duty = SERVO_MIN_DUTY + (degree * (SERVO_MAX_DUTY - SERVO_MIN_DUTY) / 180.0)
    #print("Degree: {} to {}(Duty)".format(degree,duty))
    #print('horiz duty is :', duty)
    #GPIO.setup(servo_pin_horiz,GPIO.OUT)
    servo_horiz.ChangeDutyCycle(duty)
    time.sleep(delay)
    #GPIO.setup(servo_pin_horiz,GPIO.IN)
    
    servo_horiz.stop()
    GPIO.cleanup()
    
def azi_normalization(azi):
    nor_azi = []
    for i in range(len(azi)):
        val = (azi[i] - azi[0]) * 175 / (azi[-1] - azi[0])
        nor_azi.append(val)
    
    return nor_azi

#save movement of solar (a day, per hour)
def solar_move():
    alt_angle, azi_angle = get_azinalt_interpolate('부산','20220814')
    azi_angle_normalization = azi_normalization(azi_angle)
    print('Get all angles from API')
    return alt_angle, azi_angle_normalization


def drive():
    alt_angle, azi_angle = solar_move()
    for i in range(len(alt_angle)):
        print("alt_angle is : ",int(alt_angle[i]))
        servo_control_verti(int(alt_angle[i]),0.5)
        #time.sleep(0.5)
        print("azi_angle is : ",int(azi_angle[i]))
        servo_control_horiz(int(azi_angle[i]),0.5)
        #time.sleep(0.5)
        
    servo_control_verti(0,0.5)
    servo_control_horiz(0,0.5)

    #servo_verti.stop()
    #servo_horiz.stop()
    #GPIO.cleanup()

####################################################################
def motor_drive():
    drive()

motor_drive()



