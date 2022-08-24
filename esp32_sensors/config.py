import machine
import ubinascii




# Obtenemos el ID del chip de la placa (único por dispositivo)

def obtener_id():
    return(ubinascii.hexlify(machine.unique_id()).decode('utf-8'))


DEVICE_NAME = obtener_id()

WIFI_NAME = 'realme X7 Max'
WIFI_PASSWORD = '7xuudu8z'

PIN = 23

# MQTT
SERVER = '192.168.156.108'
PORT = 1883
TOPIC = b'/max30100'

# 10 minutes
#DEEPSLEEP_TIME_MS = 10 * 60 * 1000
DEEPSLEEP_TIME_MS = 10 