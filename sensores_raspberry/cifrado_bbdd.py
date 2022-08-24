from cryptography.fernet import Fernet
clave = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
cipher_suite = Fernet(clave)
texto_cifrado = b'gAAAAABiJ4zo9YDKl2YmvwJMqXWRTa3GQZoTRCKxnEkc3M7xNtTulKK-12qhzyp_LNzWqWHrw_BNarWBvPd4y4ySd3cgLxIdnQ=='
texto_descifrado = (cipher_suite.decrypt(texto_cifrado)).decode("utf-8")         # la suite nos devuelve un literal byte y necesitamos un string


