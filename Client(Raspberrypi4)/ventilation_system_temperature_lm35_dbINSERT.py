import spidev
import time
import pymysql

def analog_read(channel):
    r = spi.xfer2([1, (0x08+channel)<<4,0])
    adc_out = ((r[1]&0x03)<<8) + r[2]
    return adc_out

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

db = None
cur = None

db = pymysql.connect(host = '10.1.0.28',user = 'root',password = '!dlwlsrb0814',db = 'mysql',charset = 'utf8')

appropriate_temperature = 20  # appropriate temperature

try:
    cur = db.cursor()
    
    while True:
        adc = analog_read(3)
        voltage = adc * 5000 /2096 # check formula
        temperature = voltage / 10.0
        print("%4d/1023 => %5.3f V => %4.1f C"%(adc,voltage,temperature))
        
        adjust_temperature = appropriate_temperature - temperature
        if adjust_temperature > 5:
            status = 'TOO COLD'
        elif adjust_temperature < -5:
            status = 'TOO HOT'
        else:
            status = 'FINE'   
            
        print('status is', status)
        
        sql = 'INSERT INTO temperature(TEMP, STATUS) VALUES (%s,%s)'
        
        cur.execute(sql,(temperature,status))
        
        db.commit()
        
        time.sleep(300) #INSERT temperature every 5 minutes
        
except KeyboardInterrupt:
    pass
finally:
    db.close()
    spi.close()
    
try:
    cur = db.cursor()
    sql = 'SELECT DATATIME, TEMP, STATUS FROM temperature'
    
    cur.execute(sql)
    
    result = cur.fetchall()
    for row in result:
        print(row[0], '|', row[1])
        
finally:
    db.close()