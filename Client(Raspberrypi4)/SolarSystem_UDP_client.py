import socket
import sys
import os
from os.path import exists

#capture by picamera
import picamera
import time
import datetime

with picamera.PiCamera() as camera:
    camera.resolution = (512,512)
    camera.start_preview()
    time.sleep(5)
    camera.stop_preview()
    camera.capture('capture.jpg')
#

 
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect(('172.20.10.13',8888))
print('connection start !')

filename = client_socket.recv(1024) #클라이언트한테 파일이름(이진 바이트 스트림 형태)을 전달 받는다
print('받은 데이터 : ', filename.decode('utf-8')) #파일 이름을 일반 문자열로 변환한다
data_transferred = 0

if not exists(filename):
    print("no file")
    sys.exit()

print("파일 %s 전송 시작" %filename)
with open(filename, 'rb') as f:
    try:
        data = f.read(1024) #1024바이트 읽는다
        while True: #데이터가 없을 때까지
            client_socket.send(data)
            #data_transferred += client_socket.send(data) #1024바이트
            data = f.read(1024)
            if not data:
                client_socket.close()
                break
    except Exception as ex:
        print(ex)
print("전송완료 %s" %(filename))
