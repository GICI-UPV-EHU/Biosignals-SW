from os import environ
from dotenv import load_dotenv
from flask import Flask, request,render_template, jsonify, send_file
import psycopg2
from psycopg2 import extras

load_dotenv()

from cryptography.fernet import Fernet
clave = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
suite_cifrado = Fernet(clave)

def cifrado_passwd():
    
    texto_cifrado = suite_cifrado.encrypt(b"*1kRzhuYj!$")   #hay que pasarlo en bytes
    return texto_cifrado

def descifrado_passwd():

    texto_cifrado = b'gAAAAABiJ4zo9YDKl2YmvwJMqXWRTa3GQZoTRCKxnEkc3M7xNtTulKK-12qhzyp_LNzWqWHrw_BNarWBvPd4y4ySd3cgLxIdnQ=='
    texto_descifrado = (suite_cifrado.decrypt(texto_cifrado)).decode("utf-8")         # la suite nos devuelve un literal byte y necesitamos un string
    return(texto_descifrado)




### crear conexión
def crear_conexion():
    
    connection = psycopg2.connect(user="sensors",
                                  password=descifrado_passwd(),
                                  host="bbdd_server",
                                  port="5432",
                                  database="sensors",
                                  sslmode='require',
                                  sslrootcert='server.crt')
    return(connection)



app = Flask(__name__)

@app.get('/usuarios')
def get_users():
    conn = crear_conexion()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM sensores")
    usuarios = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(usuarios)

@app.get('/usuarios/<usuario>')
def get_user(usuario):
    conn = crear_conexion()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM sensores where usuario = %s", (usuario,))
    usuario = cur.fetchall()
    cur.close()
    conn.close()

    if usuario is None:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    return jsonify(usuario)


@app.get('/')
def home():
    return send_file('static/index.html')


if __name__ == '__main__':
    app.run(debug=True, port=3000)
