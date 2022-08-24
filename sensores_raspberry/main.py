import connect_bbdd
# utilizamos time para crear buffer de 5 min antes de escribirlo en BBDD
import time
# necesitamos introducir timestamps en la BBDD para saber los momentos de las lecturas
from datetime import datetime, timezone
# importamos pytz porque datetime sólo trabaja con UTC y necesitamos hacer la conversión
import pytz
# Obtenemos rojo, infrarrojo y cálculo de valores
import obtener_valores
# Leemos ADC
import ADC
import psycopg2
import sys
# Trabajaremos con multiproceso en el momento de generar el buffer
# Esto lo hacemos para leer paralelamente desde el ADC y el max30102
# Además utilizaremos multiproceso también para generar el buffer y escribir en la base de datos de forma concurrente.
import multiprocessing as mpr
from multiprocessing import Process, Queue


### Introducimos una rutina previa para obtener un ID único por placa, aprovechando que cada dirección MAC de la WLAN es única por dispositivo
### Esto nos sirve como identificativo único de dispositivo y por tanto de usuario para poder hacer luego las Insert en la BBDD
import subprocess

def obtener_id():

    string="ip addr show wlan0 | grep ether| awk '{print $2}'"
    ID=subprocess.getoutput(string)
    return(ID)

#Generamos el buffer y lo llenamos el buffer con los datos de los sensores
def generar_buffer(q):

    # Obtenemos el ID, único por dispositivo
    id=str(obtener_id())
    
    ### Obtenemos valores rojo / infrarrojo en un procesador dedicado
    # Dado que disponemos de varios procesadores, vamos a aprovechar el multiproceso
    # dedicando uno de ellos a las lecturas de POX y el otro al ADC. Con los datos de ambos, los introduciremos en una cola FIFO (Queue)

    while True:
        # Tenemos que usar pytz para sacar la fecha adecuada ya que datetime sólo trabaja con UTC.
        fecha = datetime.now(pytz.timezone("Europe/Madrid"))
        
        # Hay que crear la cola FIFO con 6 datos: 
        # Usuario, rojo, infrarrojo, Pulso_SPO2, sudoracion, fecha
        # De momento introducimos sudoracion como valor ficticio según el valor ficticio obtenido con el ADC
        # El pulso y spo2 corresponden realmente a los valores de rojo e infrarrojo. Se hace media de 100 valores de cada rojo e infrarrojo en cada línea
        
        # Sirviéndonos del multiproceso, utilizamos un pool de 2 procesos para obtener valores concurrentemente del max30102 y el ADC.
        pool = mpr.Pool(processes=2)
                
        resultado_async_max30102 = pool.apply_async(obtener_valores.coger_datos).get()
        resultado_async_adc = pool.apply_async(ADC.leer_adc).get()
                       
        # resultado_async_max30102[0] tiene 100 valores de sensor rojo
        # resultado_async_max30102[1] tiene 100 valores de sensor infrarrojo
        # resultado_async_max30102[2] tiene 4 valores: Pulso obtenido de las 100 lecturas, true/false, SPO2 obtenido de las 100 lecturas y true/false.
        # Los valores de true/false son de pulso y spo2 para indicar si ha estado puesto el dedo y se han hecho lecturas.
        # resultado_async_adc tiene los valores recogidos del ADC
        datos_sensores = [id , resultado_async_max30102[0], resultado_async_max30102[1], resultado_async_max30102[2], resultado_async_adc, fecha]
        # close() llama a destruir el pool y join() espera a los procesos trabajadores.
        pool.close()
        pool.join()
        
        ### Llenamos la cola FIFO con los datos de los sensores
        q.put(datos_sensores)    
             
### Rutina principal
def main():
    
    q = Queue()
    
    #### Llenamos la cola FIFO
    llenar_buffer = Process(target=generar_buffer, args=(q,))        
    #### Vaciado de la cola FIFO 
    envio_bbdd = Process(target=connect_bbdd.insertar_sensores_bbdd_batch_queue, args=(q,))
    llenar_buffer.start()
    envio_bbdd.start()
       
  
    llenar_buffer.join()
    envio_bbdd.join()
    
## Ejecución
if __name__ == "__main__":
    main()
    