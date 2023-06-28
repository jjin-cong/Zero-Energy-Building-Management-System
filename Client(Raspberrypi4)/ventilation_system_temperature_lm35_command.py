import pymysql
import time
import RPi.GPIO as GPIO

def led(pin,t): #change code to ventilation
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    
    GPIO.output(pin,True)
    time.sleep(t)
    
    GPIO.cleanup(pin)

db = None
cur = None

try:
    while True:
        db = pymysql.connect(host = '10.1.0.28',user = 'root',password = '!dlwlsrb0814',db = 'mysql',charset = 'utf8') #connect db every step, get latest 5 data
        cur = db.cursor()

        sql = 'SELECT * FROM temperature ORDER BY DATATIME DESC LIMIT 5'
    
        cur.execute(sql)
        
        all_status = []
        
        result = cur.fetchall()
        for row in result:
            print(row[0], '|', row[1], '|', row[2])
            all_status.append(row[2])
        print('-----------')
        
        print(all_status)
        
        if all_status.count('FINE') < 3: #if 3 of 5 data is not fine, we have to change our room`s tempnmos
            print('must change tempnmos')
            
            led(18,5) #change code to ventilation
            
        time.sleep(10)
        
finally:
    db.close()