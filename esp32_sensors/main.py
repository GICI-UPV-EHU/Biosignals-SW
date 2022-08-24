import time
time.sleep(1)

import max30100
import esp
import gc
import network
import ujson

from machine import Pin
from machine import I2C
from umqtt.simple import MQTTClient

import config


gc.enable()
# esp.osdebug(None)

sda=Pin(21)
scl=Pin(22)    
        
i2c = I2C(scl=scl,sda=sda)

print('Escaneando dispositivos I2C...')
print(i2c.scan())


sensor = max30100.MAX30100(i2c=i2c)

print('Leyendo registros de MAX30100...')
print(sensor.get_registers())

sensor.enable_spo2()

print('Leyendo sensor...')

gc.collect() 
#client = MQTTClient(config.DEVICE_NAME, config.SERVER, config.PORT)
#client.connect()

#while 1:


    #for count in range(1000):  
sensor.read_sensor()
medir = {
            "dispositivo": config.DEVICE_NAME,
            "infrarojo": sensor.ir,
            "rojo": sensor.red
        }
#time.sleep(0.5)
msg = ujson.dumps(medir)
print(msg)
 
#client.publish(config.TOPIC, msg)

gc.collect()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

while not wlan.isconnected():
    wlan.connect(config.WIFI_NAME, config.WIFI_PASSWORD)
    time.sleep(1)

    count = 0
    while not wlan.isconnected() and count < 10:
        count += 1
        time.sleep(1)

time.sleep(1)
machine.deepsleep(config.DEEPSLEEP_TIME_MS)
