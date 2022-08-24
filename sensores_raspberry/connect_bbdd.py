import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
import psycopg2.extras as extras
import ssl
import cifrado_bbdd
from io import StringIO
import os
import sys
import pandas as pd
from multiprocessing import Process, Queue


def connectar_bbdd():
    connection = psycopg2.connect(user="sensors",
                                      password=cifrado_bbdd.texto_descifrado,
                                      host="rpsensors.com",
                                      port="5432",
                                      database="sensors",
                                      sslmode = 'require',
                                      sslrootcert = '/home/pi/.certs/postgresql.crt')
    return(connection)

def cerrar_conexion(conn):
    cursor = conn.cursor()
    cursor.close()
    conn.close()
    print("Cerrada la conexión a la BBDD\n")
    

### Buscamos todos los registros
def obtener_datos_sensores_total(userID):
    try:
        connection = psycopg2.connect(user="sensors",
                                      password=cifrado_bbdd.texto_descifrado,
                                      host="rpsensors.com",
                                      port="5432",
                                      database="sensors",
                                      sslmode = 'require',
                                      sslrootcert = '/home/pi/.certs/postgresql.crt')

        print("Lanzamos la query...")
        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from sensores"

        cursor.execute(postgreSQL_select_Query)
        registros_usuario = cursor.fetchall()
        print("Usuario    Rojo    Infrarrojo    Pulso-SPO2       Sudoración          Fecha")
        print("---------------------------------------------------------------------------")
        for row in registros_usuario:
            print(row[0],"  ", row[1],"  ", row[2],"  ", row[3],"  ", row[4],"  ", row[5])
            
    except (Exception, psycopg2.Error) as error:
        print("Error obteniendo datos de la tabla de PostgreSQL", error)

    finally:
        # Cerramos la conexión a la BBDD
        if connection:
            cursor.close()
            connection.close()
            print("Cerrada la conexión a la BBDD\n")


### Buscamos datos de sensores en las tablas por usuario
def obtener_datos_sensores_usuario(userID):
    try:
        connection = psycopg2.connect(user="sensors",
                                      password=cifrado_bbdd.texto_descifrado,
                                      host="rpsensors.com",
                                      port="5432",
                                      database="sensors",
                                      sslmode = 'require',
                                      sslrootcert = '/home/pi/.certs/postgresql.crt')

        print("Lanzamos la query...")
        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from sensores where usuario = %s"

        cursor.execute(postgreSQL_select_Query, (userID,))
        registros_usuario = cursor.fetchall()
        print("Usuario    Rojo    Infrarrojo    Pulso-SPO2       Sudoración          Fecha")
        print("---------------------------------------------------------------------------")
        for row in registros_usuario:
            print(row[0],"  ", row[1],"  ", row[2],"  ", row[3],"  ", row[4],"  ", row[5])

    except (Exception, psycopg2.Error) as error:
        print("Error obteniendo datos de la tabla de PostgreSQL", error)

    finally:
        # Cerramos la conexión a la BBDD
        if connection:
            cursor.close()
            connection.close()
            print("Cerrada la conexión a la BBDD\n")



def insertar_datos_sensores(datos_sensores,connection):
        print("Lanzamos la query...")
        cursor = connection.cursor()
        postgreSQL_insert_Query = "INSERT INTO sensores (usuario, rojo, infrarrojo, pulso_spo2, sudoracion, fecha) VALUES (%s,%s,%s,%s,%s,%s);"
        cursor.execute(postgreSQL_insert_Query, datos_sensores)
        connection.commit()


### Buscamos datos de sensores en las tablas por usuario
def insertar_datos_sensores_usuario(usuario, rojo, infrarrojo, pulso_spo2, sudoracion, fecha):
    try:
        connection = psycopg2.connect(user="sensors",
                                      password=cifrado_bbdd.texto_descifrado,
                                      host="rpsensors.com",
                                      port="5432",
                                      database="sensors",
                                      sslmode = 'require',
                                      sslrootcert = '/home/pi/.certs/postgresql.crt')

        print("Lanzamos la query...")
        cursor = connection.cursor()
        postgreSQL_insert_Query = "INSERT INTO sensores (usuario, rojo, infrarrojo, pulso_spo2, sudoracion, fecha) VALUES (%s,%s,%s,%s,%s,%s)"

        cursor.execute(postgreSQL_insert_Query, (usuario, rojo, infrarrojo, pulso_spo2, sudoracion, fecha))
        #registros_usuario = cursor.fetchall()
        connection.commit()


            
    except (Exception, psycopg2.Error) as error:
        print("Error obteniendo datos de la tabla de PostgreSQL", error)

    finally:
        # Cerramos la conexión a la BBDD
        if connection:
            cursor.close()
            connection.close()
            print("Cerrada la conexión a la BBDD\n")

#Insertamos los datos de los sensores en el buffer

def insertar_sensores_bbdd(buffer):
    x=0
    ### Hacemos que se abra y cierre la conexión a la BBDD una única vez para todas las inserts.
    try:
        connection = psycopg2.connect(user="sensors",
                                      password=cifrado_bbdd.texto_descifrado,
                                      host="rpsensors.com",
                                      port="5432",
                                      database="sensors",
                                      sslmode = 'require',
                                      sslrootcert = '/home/pi/.certs/postgresql.crt')

        print("Lanzamos la query...")
        cursor = connection.cursor()
        #Recorremos el buffer línea a linea para insertarlas en la BBDD
        for i in buffer:
            ## Tenemos un  array de líneas, recorremos línea por línea
            linea=buffer[x]
            # Por cada línea, sacamos ahora los elementos individuales
            usuario=str(linea[0])
            rojo=str(linea[1])
            infrarrojo=str(linea[2])
            pulso_spo2=str(linea[3])
            sudoracion=str(linea[4])
            fecha=str(linea[5])
            postgreSQL_insert_Query = "INSERT INTO sensores (usuario, rojo, infrarrojo, pulso_spo2, sudoracion, fecha) VALUES (%s,%s,%s,%s,%s,%s);"
            cursor.execute(postgreSQL_insert_Query, (usuario, rojo, infrarrojo, pulso_spo2, sudoracion, fecha))
            connection.commit()
            x+=1
        
    except (Exception, psycopg2.Error) as error:
        print("Error obteniendo datos de la tabla de PostgreSQL", error)

    finally:
        # Cerramos la conexión a la BBDD
        if connection:
            cursor.close()
            connection.close()
            print("Cerrada la conexión a la BBDD\n")


#### Este método es mucho más rápido con las inserts, tal y como hemos extraído de la documentación del driver psycopg2
def insertar_sensores_bbdd_batch(buffer): 

    x=0
    ### Hacemos que se abra y cierre la conexión a la BBDD una única vez para todas las inserts.
    try:
        connection = psycopg2.connect(user="sensors",
                                      password=cifrado_bbdd.texto_descifrado,
                                      host="rpsensors.com",
                                      port="5432",
                                      database="sensors",
                                      sslmode = 'require',
                                      sslrootcert = '/home/pi/.certs/postgresql.crt')

        print("Lanzamos la query...")
        cursor = connection.cursor()
        #Recorremos el buffer línea a linea para insertarlas en la BBDD
        for i in buffer:
            ## Tenemos un  array de líneas, recorremos línea por línea
            linea=buffer[x]
            # Por cada línea, sacamos ahora los elementos individuales
            usuario=str(linea[0])
            rojo=str(linea[1])
            infrarrojo=str(linea[2])
            pulso_spo2=str(linea[3])
            sudoracion=str(linea[4])
            fecha=str(linea[5])

            postgreSQL_insert_Query = "INSERT INTO sensores (usuario, rojo, infrarrojo, pulso_spo2, sudoracion, fecha) VALUES (%s,%s,%s,%s,%s,%s);"

            valores=[(usuario, rojo, infrarrojo, pulso_spo2, sudoracion, fecha)]
            psycopg2.extras.execute_batch(cursor, postgreSQL_insert_Query, valores)
             
            connection.commit()
            x+=1
        
    except (Exception, psycopg2.Error) as error:
        print("Error obteniendo datos de la tabla de PostgreSQL", error)

    finally:
        # Cerramos la conexión a la BBDD
        if connection:
            cursor.close()
            connection.close()
            print("Cerrada la conexión a la BBDD\n")
    


def copy_usando_stringio(conn, buffer):
    """
    Here we are going save the dataframe in memory 
    and use copy_from() to copy it to the table
    """
    # save dataframe to an in memory buffer
    
    df = pd.DataFrame(buffer)    
    buff = StringIO()
    buffer.to_csv(buff, index_label='usuario', header=False)
    #df.to_csv(buff, index_label='usuario', header=False)
    buff.seek(0)
    
    tabla = 'sensores'
    
    cursor = conn.cursor()
    try:
        cursor.copy_from(buffer, tabla, sep=",")
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("fin copy_usando_stringio()")
    cursor.close()

 

def insertar_sensores_bbdd_batch_queue(q): 

    x=0
    ### Hacemos que se abra y cierre la conexión a la BBDD una única vez para todas las inserts.
    try:
        connection = psycopg2.connect(user="sensors",
                                      password=cifrado_bbdd.texto_descifrado,
                                      host="rpsensors.com",
                                      port="5432",
                                      database="sensors",
                                      sslmode = 'require',
                                      sslrootcert = '/home/pi/.certs/postgresql.crt')

        print("Lanzamos la query...")
        cursor = connection.cursor()
        #Recorremos el buffer línea a linea para insertarlas en la BBDD
        while True:
            # Sacamos cada una línea de la cola FIFO
            linea = q.get()
            # Por cada línea, sacamos ahora los elementos individuales
            usuario=str(linea[0])
            rojo=str(linea[1])
            infrarrojo=str(linea[2])
            pulso_spo2=str(linea[3])
            sudoracion=str(linea[4])
            fecha=str(linea[5])
            # Preparamos la query con la insert
            postgreSQL_insert_Query = "INSERT INTO sensores (usuario, rojo, infrarrojo, pulso_spo2, sudoracion, fecha) VALUES (%s,%s,%s,%s,%s,%s);"
            # Insert con execute_batch
            valores=[(usuario, rojo, infrarrojo, pulso_spo2, sudoracion, fecha)]
            psycopg2.extras.execute_batch(cursor, postgreSQL_insert_Query, valores)
            connection.commit()
            x+=1
                
            if linea is None:
                break
    except (Exception, psycopg2.Error) as error:
        print("Error obteniendo datos de la tabla de PostgreSQL", error)

    finally:
        # Cerramos la conexión a la BBDD
        if connection:
            cursor.close()
            connection.close()
            print("Cerrada la conexión a la BBDD\n")
            
            

### Pequeña gema de la documentación de psycopg2.extras. Método que me da el máximo rendimiento utilizando esta librería.            
def insertar_sensores_bbdd_values_queue(q): 

    x=0
    ### Hacemos que se abra y cierre la conexión a la BBDD una única vez para todas las inserts.
    try:
        connection = psycopg2.connect(user="sensors",
                                      password=cifrado_bbdd.texto_descifrado,
                                      host="rpsensors.com",
                                      port="5432",
                                      database="sensors",
                                      sslmode = 'require',
                                      sslrootcert = '/home/pi/.certs/postgresql.crt')

        print("Lanzamos la query...")
        cursor = connection.cursor()
        #Recorremos el buffer línea a linea para insertarlas en la BBDD
        
        while True:
            # get a unit of work
            linea = q.get()
            # check for stop
            # Por cada línea, sacamos ahora los elementos individuales
            usuario=str(linea[0])
            rojo=str(linea[1])
            infrarrojo=str(linea[2])
            pulso_spo2=str(linea[3])
            sudoracion=str(linea[4])
            fecha=str(linea[5])

            postgreSQL_insert_Query = "INSERT INTO sensores (usuario, rojo, infrarrojo, pulso_spo2, sudoracion, fecha) VALUES (%s,%s,%s,%s,%s,%s);"

            valores=[(usuario, rojo, infrarrojo, pulso_spo2, sudoracion, fecha)]
            psycopg2.extras.execute_values(cursor, postgreSQL_insert_Query, valores)
             
            connection.commit()
            x+=1
                
            if linea is None:
                break
        
    except (Exception, psycopg2.Error) as error:
        print("Error obteniendo datos de la tabla de PostgreSQL", error)

    finally:
        # Cerramos la conexión a la BBDD
        if connection:
            cursor.close()
            connection.close()
            print("Cerrada la conexión a la BBDD\n")
        

            



