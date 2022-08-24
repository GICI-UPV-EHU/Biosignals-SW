import time
# Importamos el módulo del ADC
import Adafruit_ADS1x15

def leer_adc():

    # Creamos una instancia ADS1115 ADC (16-bit).
    # Lo seteamos en el bus1, 0x48.
    adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

    # Elegimos una ganancia de 1 para leer voltajes de 0 a 4.09V.
    # Ver la tabla 3 del datasheet ADS1015/ADS1115 para otros valores.
    GAIN = 1

    # Sólo cogemos A0. No necesitamos más para el GSR.
    values = [0]*1
    for i in range(1):
        # Dado el rango de 1, leemos sólo A0 con la ganancia especificada
        values[i] = adc.read_adc(i, gain=GAIN)

    # Guardamos los valores formateados
    valores_adc = '{0:>6}'.format(*values)
    return (valores_adc)



