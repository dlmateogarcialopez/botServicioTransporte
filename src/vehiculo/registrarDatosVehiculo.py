from time import sleep
import json
import os
import sys
informacion_vehiculo = {} #Almacenar información temporal de vehiculo que se registra
vehiculos_registrados = [] #Almacenar todos los vehículos que se van registrando en el bot
class Vehiculo:

    def __init__(self):
        ...


    def solicitarCorreoElectronico(data, bot):

        record = Record()

        documentoPopietario = data.text
    
        record.documentoPopietario = documentoPopietario

        informacion_vehiculo[data.chat.id] = record

        Vehiculo.enviarAccionEscribiendo(data, bot)
        respuesta = bot.reply_to(data, 'Ingresa por favor el correo electrónico del propietario del vehículo')

        return respuesta

    def obtenerClaveObjeto(record, clave, data):
        if clave == 'correoPropietario':
            record.correoPropietario = data.text
        elif clave == 'nombrePropietario':
            record.nombrePropietario = data.text
        elif clave == 'placaVehiculo':
            record.placaVehiculo = data.text       
        elif clave == 'descripcioVehiculo':
            record.descripcioVehiculo = data.text   
        elif clave == 'nivelAceite':
            record.nivelAceite = data.text  
        elif clave == 'nivelLiquidoFrenos':
            record.nivelLiquidoFrenos = data.text   
        elif clave == 'nivelRefrigerante':
            record.nivelRefrigerante = data.text      
        elif clave == 'nivelLiquidoDireccion':
            record.nivelLiquidoDireccion = data.text 
        elif clave == 'soat':
            record.soat = data.text      
        elif clave == 'seguroContractual':
            record.seguroContractual = data.text      
        elif clave == 'seguroExtraContrActual':
            record.seguroExtraContrActual = data.text

    def solicitarDatos(data, bot, mensaje, clave):        

        record = informacion_vehiculo[data.chat.id]

        Vehiculo.obtenerClaveObjeto(record, clave, data)

        Vehiculo.enviarAccionEscribiendo(data, bot)
        
        respuesta = bot.reply_to(data, mensaje)

        return respuesta

    def enviarAccionEscribiendo(data, bot):
            bot.send_chat_action(data.chat.id, 'typing')
            sleep(1)        
                                                                                       

    def almacenarDatosVehiculo(data, bot):

        fotoSeguroExtraContractual = data.text

        record = informacion_vehiculo[data.chat.id]
        record.seguroExtraContrActual = fotoSeguroExtraContractual    

        datosCompletos = Vehiculo.validarDatosCompletos(record)
        if(datosCompletos):
            #Asignar el mecanico al vegiculo   
            mecanicoAsignado = Vehiculo.seleccionarMecanicoDisponible()         
            record.mecanicoAsignado = mecanicoAsignado

            #Almacenar información del vehículo
            vehiculos_registrados.append(record)
            bot.reply_to(data, 'Registro exitoso')

    #Buscar mecánico disponible para ser asignado
    def seleccionarMecanicoDisponible():
        with open(os.path.join(sys.path[0], 'vehiculo/mecanico.json'), "r") as contenido:
            data = json.load(contenido)

        mecanicos = data['mecanicos']
        for mecanico in mecanicos:
            if mecanico['disponibilidad']:
                return mecanico['documento']


    def validarExistenciaDocumento(data):
        if data.text == '123':

            record = Record()

            informacion_vehiculo[data.chat.id] = record

            datosVehiculo = informacion_vehiculo[data.chat.id]
            datosVehiculo.documentoPopietario = data.text
            datosVehiculo.correoPropietario = "correo@gmail.com"
            datosVehiculo.nombrePropietario = "Nombre existente"

            return True
        else:
            return False

    def validarExistenciaPlaca(data):
        if data.text == 'hqd69f':
            return True
        else:
            return False 

    def validarExistenciaCorreoElectronico(data):
        if data.text == 'correo@gmail.com':
            return True
        else:
            return False             

    def mostrarMenuPrincipal(data, bot, types, msg):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

            itembtn1 = types.KeyboardButton('Registrar datos de vehiculo')
            itembtn2 = types.KeyboardButton('Registrar líquidos y repuestos')
            itembtn3 = types.KeyboardButton('Históricos')
            itembtn4 = types.KeyboardButton('Seguros')

            markup.row(itembtn1)
            markup.row(itembtn2)
            markup.row(itembtn3)
            markup.row(itembtn4)
            #markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
        
            bot.send_message(data.chat.id, msg, reply_markup=markup)                       

    def validarOpcionDeRegistro(bot, types, message):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

        itembtn1 = types.KeyboardButton('Registrar datos de vehiculo')
        itembtn2 = types.KeyboardButton('Continuar con el registro actual')

        markup.row(itembtn1)
        markup.row(itembtn2)
    
        bot.send_message(message.chat.id, "Este número de documento ya existe en el sistema, ¿te gustaría continuar el registro del vehículo con un los datos almacenados o te gustaría realizar un nuevo registro ?:", reply_markup=markup)

    def validarDatosCompletos(data):

        if data.documentoPopietario == None:
            return False
        
        if data.correoPropietario == None:
            return False

        if data.nombrePropietario == None:
            return False

        if data.placaVehiculo == None:
            return False

        if data.descripcioVehiculo == None:
            return False

        if data.nivelAceite == None:
            return False

        if data.nivelLiquidoFrenos == None:
            return False

        if data.nivelRefrigerante == None:
            return False

        if data.nivelLiquidoDireccion == None:
            return False

        if data.soat == None:
            return False

        if data.seguroContractual == None:
            return False

        if data.seguroExtraContrActual == None:
            return False

        return True


class Record:
    def __init__(self):
        self.documentoPopietario = None
        self.correoPropietario = None
        self.nombrePropietario = None
        self.placaVehiculo = None
        self.descripcioVehiculo = None
        self.nivelAceite = None
        self.nivelLiquidoFrenos = None
        self.nivelRefrigerante = None
        self.nivelLiquidoDireccion = None
        self.soat = None
        self.seguroContractual = None
        self.seguroExtraContrActual = None
        self.mecanicoAsignado = None

