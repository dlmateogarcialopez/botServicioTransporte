from time import sleep
import json
import os
import sys
from vehiculo.registrarDatosVehiculo import vehiculos_registrados
from telebot import types
from config import bot
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


informacion_liquidoRepuestos = {}
informacion_liquidoRepuestos_registrados = []
lista_placas = []
mi_path = "placas.txt"
placa_actual = {'placa':'sinPlaca'}

class LiqudosRepuestos:

    def __init__(self):        
        ...
        
    
    def traerListaVehiculos():
        #lista_placas = []
        with open(mi_path, "r") as archivo:
            #print(archivo.readlines())
            for linea in archivo:
                linea_limpia = linea.rstrip('\n')
                lista_placas.append(linea_limpia)
            #lista_placas.append(archivo.readline())
        
        
    def mostrarMenuPrincipal(data, bot, types, msg):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

            itembtn1 = types.KeyboardButton('Registrar datos de vehículo')
            itembtn2 = types.KeyboardButton('Registrar líquidos y repuestos')
            itembtn3 = types.KeyboardButton('Históricos')
            itembtn4 = types.KeyboardButton('Seguros')

            markup.row(itembtn1)
            markup.row(itembtn2)
            markup.row(itembtn3)
            markup.row(itembtn4)
            #markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
        
            bot.send_message(data.chat.id, msg, reply_markup=markup)  
    
    def enviarAccionEscribiendo(data, bot):
            bot.send_chat_action(data.chat.id, 'typing')
            sleep(1)    

    def validarExistenciaPlaca(data):
        lista_placas.clear()
        LiqudosRepuestos.traerListaVehiculos()
        placa_upper = data.text.upper()
        if placa_upper in lista_placas:
            return True
        else:
            return False 
    
    def obtenerClaveObjeto(record, clave, data):
        if clave == 'placaVehiculo':
            record.placaVehiculo = data.text.upper()  
            print("ingreso a obtener calve objeto placa")     
        elif clave == 'nivelAceite':
            record.nivelAceite = data.text  
        elif clave == 'nivelLiquidoFrenos':
            record.nivelLiquidoFrenos = data.text   
        elif clave == 'nivelRefrigerante':
            record.nivelRefrigerante = data.text      
        elif clave == 'nivelLiquidoDireccion':
            record.nivelLiquidoDireccion = data.text 
        elif clave == 'cambioRepuestos':
            record.cambioRepuestos = data.text 
        elif clave == 'cedulaMecanico':
            record.cedulaMecanico = data.text 
            
       

    def solicitarDatos(data, bot, mensaje, clave):        
        record = informacion_liquidoRepuestos[data.chat.id]

        LiqudosRepuestos.obtenerClaveObjeto(record, clave, data)

        LiqudosRepuestos.enviarAccionEscribiendo(data, bot)
        
        respuesta = bot.reply_to(data, mensaje)

        return respuesta

    def almacenarDatos(data, bot):
        
        cambioRepuestos = data.text

        record = informacion_liquidoRepuestos[data.chat.id]
        record.cambioRepuestos = cambioRepuestos    

        datosCompletos = LiqudosRepuestos.validarDatosCompletos(record)
        if(datosCompletos):           
            #Almacenar información de los liquidos y repuestos
            informacion_liquidoRepuestos_registrados.append(record)   
            # Se llama al metódo que notifica al dueño del vevículo
            LiqudosRepuestos.enviarCorreo(data)            

            bot.reply_to(data, 'Registro de líquidos y repuestos exitoso')


    def validarDatosCompletos(data):

        if data.placaVehiculo == None:
            return False

        if data.nivelAceite == None:
            return False

        if data.cedulaMecanico == None:
            return False

        if data.nivelLiquidoFrenos == None:
            return False

        if data.nivelRefrigerante == None:
            return False

        if data.nivelLiquidoDireccion == None:
            return False

        if data.cambioRepuestos == None:
            return False

        return True
    
    def solicitarPlaca(data, bot):

        record = Record()

        placaVehiculo = data.text.upper()
        print("acaaa", placaVehiculo)
    
        record.placaVehiculo = placaVehiculo

        informacion_liquidoRepuestos[data.chat.id] = record

        LiqudosRepuestos.enviarAccionEscribiendo(data, bot)
        respuesta = bot.reply_to(data, 'Ingresa por favor el nivel de aceite del vehículo')

        return respuesta

    def solicitarCedulaMecanico(data, bot):

        record = Record()

        placaVehiculo = data.text.upper()
        placa_actual['placa'] = placaVehiculo
    
        record.placaVehiculo = placaVehiculo

        informacion_liquidoRepuestos[data.chat.id] = record

        LiqudosRepuestos.enviarAccionEscribiendo(data, bot)

        respuesta = bot.send_message(data.chat.id, 'Ingresa por favor el documento del mécanico asignado al vehículo')
        bot.register_next_step_handler(respuesta, LiqudosRepuestos.validarMecanicoPlaca)

        #respuesta = bot.reply_to(data, 'Ingresa por favor el documento del mécanico asignado al vehículo')
        #return respuesta

    def validarMecanicoPlaca(data):
        if len(vehiculos_registrados) > 0:           
            for vehiculo in vehiculos_registrados:
                if vehiculo.placaVehiculo.upper() == placa_actual['placa'] and (vehiculo.mecanicoAsignado == data.text):
                    #Persiste la respuesta ingresada por el usuario y retorna la respuesta
                    respuesta =  LiqudosRepuestos.solicitarDatos(data, bot, 'Ingresa por favor el nivel de aceite del vehículo', 'cedulaMecanico')
                
                    #Se llama al metodo register_next_step_handler para continuar con la conversación 
                    bot.register_next_step_handler(respuesta, LiqudosRepuestos.solicitarNivelLiquidosFreno)
                    return                
            LiqudosRepuestos.mostrarMenuPrincipal(data, bot, types, "No se puede realizar el registro debido a que el mecanico ingresado no tiene asignado el vehículo, selecciona una opción:")            
        else:
            LiqudosRepuestos.mostrarMenuPrincipal(data, bot, types, "No se encontró ningún vehículo, selecciona una opción:")  


    def solicitarNivelLiquidosFreno(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  LiqudosRepuestos.solicitarDatos(message, bot, 'Ingresa por favor el nivel de líquido de frenos del vehículo', 'nivelAceite')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, LiqudosRepuestos.solicitarNivelLiquidosRefrigerante)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}") 

    def solicitarNivelLiquidosRefrigerante(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  LiqudosRepuestos.solicitarDatos(message, bot, 'Ingresa por favor el nivel de refrigerante del vehículo', 'nivelLiquidoFrenos')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, LiqudosRepuestos.solicitarNivelLiquidosDireccion)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")       

    def solicitarNivelLiquidosDireccion(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  LiqudosRepuestos.solicitarDatos(message, bot, 'Ingresa por favor el nivel de liquidos de dirección del vehículo', 'nivelRefrigerante')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, LiqudosRepuestos.solicitarCambiosRepuesto)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")       

    def solicitarCambiosRepuesto(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  LiqudosRepuestos.solicitarDatos(message, bot, 'Ingresa por favor los cambios de repuestos realizados al vehículo', 'nivelLiquidoDireccion')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, LiqudosRepuestos.almacenarDatosDeLiquidosRepuestos)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")   

    def almacenarDatosDeLiquidosRepuestos(message):
        try:

            #almacenar respuesta, en la base de datos
            LiqudosRepuestos.almacenarDatos(message, bot)
            
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")   

    def enviarCorreo(data):
        if len(vehiculos_registrados) > 0:           
            for vehiculo in vehiculos_registrados:
                if vehiculo.placaVehiculo.upper() == placa_actual['placa']:
                    correo = vehiculo.correoPropietario

                    msg = MIMEMultipart()
                    # cuerpo del mensaje
                    message =  "Señor(a) propietari@ " + vehiculo.nombrePropietario + " el presente correo es para notificarle sobre el nuevo registro de líquidos y cambio de repuestos para el vehículo de placas: " + vehiculo.placaVehiculo + ". Información registrada por el mécanico: " + vehiculo.mecanicoAsignado + ". Para revisar el historial, por favor ingrese al chat"

                    # los parametros del correo remitente
                    password = "bduaovijjfgfnzma"
                    msg['From'] = "laulopez0204@gmail.com"
                    msg['To'] = correo
                    msg['Subject'] = "Registro de líquidos y repuestos"

                    # se adiciona al cuerpo del correo
                    msg.attach(MIMEText(message, 'plain'))

                    #servidor y puerto
                    server = smtplib.SMTP('smtp.gmail.com: 587')
                    server.starttls()

                    # se cargan las credenciales
                    server.login(msg['From'], password)

                    try:
                        # se envía el correo através del servidor 
                        server.sendmail(msg['From'], msg['To'], msg.as_string())
                        server.quit()
                        bot.reply_to(data, f"Correo enviado correctamente a %s:" % (msg['To']))   
                        #print "Correo enviado correctamente a %s:" % (msg['To'])            
                    except Exception as e:
                        bot.reply_to(message, f"Algo terrible sucedió. No se envió el correo: {e}")
                    


class Record:
    def __init__(self):
        self.placaVehiculo = None
        self.nivelAceite = None
        self.nivelLiquidoFrenos = None
        self.nivelRefrigerante = None
        self.nivelLiquidoDireccion = None
        self.cambioRepuestos = None
        self.cedulaMecanico = None