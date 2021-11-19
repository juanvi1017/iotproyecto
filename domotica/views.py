import logging
from types import TracebackType
from django.shortcuts import render
from django.views import generic
import requests
import json
from django.http import HttpResponse
#-------------------------------- Criptografia
from Crypto.Cipher import AES
import base64
from Crypto import Random
import hashlib
#------------------------------- Entorno
from dotenv import load_dotenv
from os import getenv


load_dotenv()
environment = getenv('ENVIRONMENT_USUARIO_RT', 'iot') 

# VARIABLES DE CONEXIÓN
if environment == 'iot':
    #Generador de la clave y se guarda en un archivo .pem
    '''
    key=Random.new().read(AES.block_size)#Llave en bytes
    key=hashlib.sha256(key).digest()
    key=base64.b64encode(key)
    f = open('C:/Users/juanvi/Documents/mykey.pem','wb')
    f.write(key)
    f.close()
    '''

    #Leo la llave almacenada en el archivo .pem
    #f = open('C:/Users/juanvi/Documents/mykey.pem','r')
    f = open('static/mykey.pem','r')
    key=f.read()
    key=base64.b64decode(key)
    diccionario={'true':'americana1.#1', 'false':'americana1.#0'}
    
#-----------------------------------------------------------------------------------



def home(request):
   
    return render(request, "domotica/templates/index.html")


def cifrar(request):
    if request.method == 'POST':
        try:
            info = request.POST["mensaje"]
            mensaje=diccionario[info]
            mensaje=mensaje.encode()#cambio el mensaje de string a bytes
            cipher = AES.new(key, AES.MODE_EAX) #creo el cifrado con la llave
            nonce=cipher.nonce
            nonce=base64.b64encode(nonce)
            nonce=nonce.decode()
            encryptor = cipher.encrypt(mensaje)#encripto el mensaje
            encoded_encrypted_msg = base64.b64encode(encryptor)#modifico el byte encriptado a un formato base 64  o utf-8 o latin -1
            encoded_encrypted_msg=encoded_encrypted_msg.decode()#el mensaje encriptado cambio el tipo de dato de byte a string para poder enviarlo por json
            responseData = {
            'result': encoded_encrypted_msg,
            'nonce':nonce
            }
            return HttpResponse(json.dumps(responseData), content_type="application/json")
        except Exception as e:
            print(e)
            print("Error al cifrar")
            return None
    
   

def decifrar(request): 
    if request.method == 'POST':
        try:
            msj=bool()
            mensaje = request.POST["mensaje"]
            nonce=request.POST["nonce"]
            nonce=nonce.encode()
            nonce=base64.b64decode(nonce)
            mensaje=mensaje.encode()#cambio el mensaje de string a byte
            mensaje = base64.b64decode(mensaje)#devuelvo en mensaje al formato original de la encriptacion
            decryptor = AES.new(key, AES.MODE_EAX, nonce)
            decrypted = decryptor.decrypt(mensaje)
            decrypted=decrypted.decode()#cambio el mensaje desencriptado de byte a string
            if decrypted== "americana1.#1":
                msj=True 
            else:
                msj=False
            responseData = {
            'result': msj,
            }
            return HttpResponse(json.dumps(responseData), content_type="application/json")
        except Exception as e:
            print(e)
            print("Error al decifrar")
            return None