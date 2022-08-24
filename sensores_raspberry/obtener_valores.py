
import sys
import multiprocessing as mpr

### importamos las librerías de sensores. Creamos un paquete
sys.path.insert(0, '/home/oinatz/TFM_Bio/sensores_raspberry/max30102/')
import max30102
import hrcalc
###


m = max30102.MAX30102()

# Se utilizan 100 muestras para calcular HR/SpO2 en cada loop
    
def coger_datos():
    #while True:
    red, ir = m.read_sequential()
    pulso_spo2 = hrcalc.calc_hr_and_spo2(ir, red)
    
    ### Convertimos las listas a string
    
    #lista_red_str = [str(i) for i in red]
    #lista_ir_str = [str(i) for i in ir]
    lista_pulso_spo2_str = [str(i) for i in pulso_spo2]
     
    
    ### Con los elementos en string, hacemos las joins cambiando el separador. El motivo es para luego utilizar copy_from como método
    ### más eficiente posible para hacer las inserts en la base de datos.
    #string_red = ";".join(lista_red_str)
    #string_ir = ";".join(lista_ir_str)
    #string_pulso_spo2 = ";".join(lista_pulso_spo2_str)
    
    
    # Para hacer posteriormente el copy a la BBDD, tenemos que reemplazar el delimitador de las listas.
    
        
    ## Se devuelven 100 lecturas de rojo y 100 de infrarrojo en cada iteración (1s)
    ## Además de los cálculos de pulso y spo2 realizados en cada iteración que tiene esas 100 lecturas
    return (red, ir, lista_pulso_spo2_str)

