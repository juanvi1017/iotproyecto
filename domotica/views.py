from django.shortcuts import render
from django.views import generic
import requests
import json
from django.http import HttpResponse
#-------------------------------- Criptografia
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import ast
import base64
#------------------------------- Entorno
from dotenv import load_dotenv
from os import getenv


load_dotenv()
environment = getenv('ENVIRONMENT_USUARIO', 'iot') 

# VARIABLES DE CONEXIÓN
if environment == 'iot':
    #Generador de la clave y se guarda en un archivo .pem
    '''
    key = RSA.generate(2048)
    f = open('C:/djangoPersonal/mykey.pem','wb')
    f.write(key.export_key('PEM'))
    f.close()
    '''

    #Leo la llave almacenada en el archivo .pem
    f = open('static/mykey.pem','r')
    key = RSA.import_key(f.read())
#-----------------------------------------------------------------------------------



def home(request):
   
    return render(request, "domotica/templates/index.html")


def cifrar(request):
    if request.method == 'GET':
        mensaje = request.GET["mensaje"]
        mensaje=mensaje.encode()#cambio el mensaje de string a bytes
        encryptor = PKCS1_OAEP.new(key)#le digo con que llave se va a encriptar
        encrypted = encryptor.encrypt(mensaje)#encripto el mensaje
        encoded_encrypted_msg = base64.b64encode(encrypted)#codifico el byte encriptado a un formato base 64  o utf-8 o latin -1
        encoded_encrypted_msg=encoded_encrypted_msg.decode()#el mensaje encriptado cambio el tipo de dato de byte a string para poder enviarlo por json
        responseData = {
        'result': encoded_encrypted_msg,
         }
        return HttpResponse(json.dumps(responseData), content_type="application/json")
    
   

def decifrar(request): 
    if request.method == 'GET':
        msj=bool()
        mensaje = request.GET["mensaje"]
        mensaje=mensaje.encode()#cambio el mensaje de string a byte
        mensaje = base64.b64decode(mensaje)#devuelvo en mensaje al formato original de la encriptacion
        decryptor = PKCS1_OAEP.new(key)
        decrypted = decryptor.decrypt(ast.literal_eval(str(mensaje)))#desencripto el mensaje
        decrypted=decrypted.decode()#cambio el mensaje desencriptado de byte a string
        if decrypted== "true":
            msj=True
        else:
            msj=False
        responseData = {
        'result': msj,
        }
        return HttpResponse(json.dumps(responseData), content_type="application/json")