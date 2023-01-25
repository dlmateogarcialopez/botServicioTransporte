from time import sleep
import json
import os
import sys
from telebot import types
from config import bot
from vehiculo.vehiculoDb import VehiculoDb
from vehiculo.implementaciones import LectorFuenteDatos
informacion_vehiculo = {} #Almacenar información temporal de vehiculo que se registra
#vehiculos_registrados = [] #Almacenar todos los vehículos que se van registrando en el bot
vehiculoDb = VehiculoDb(LectorFuenteDatos())
mi_path = "placas.txt"

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
            #vehiculos_registrados.append(record)
            vehiculoDb.guardarVehiculo(record)

            with open(mi_path, 'a+') as f:
                f.write(record.placaVehiculo.upper() + '\n')

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
        vehiculos = vehiculoDb.consultarVehiculos()
        for vehiculo in vehiculos:
            if vehiculo.documentoPopietario == data.text:

                record = Record()

                informacion_vehiculo[data.chat.id] = record

                datosVehiculo = informacion_vehiculo[data.chat.id]
                datosVehiculo.documentoPopietario = data.text
                datosVehiculo.correoPropietario = "correo@gmail.com"
                datosVehiculo.nombrePropietario = "Nombre existente"
                return True

        return False

    def validarExistenciaPlaca(data):
        vehiculos = vehiculoDb.consultarVehiculos()
        for vehiculo in vehiculos:
            if vehiculo.placaVehiculo == data.text:
                return True
        return False 

    def validarExistenciaCorreoElectronico(data):
        vehiculos = vehiculoDb.consultarVehiculos()
        for vehiculo in vehiculos:
            if vehiculo.correoPropietario == data.text:
                return True
        return False            

    def mostrarMenuPrincipal(data, bot, types, msg):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

            itembtn1 = types.KeyboardButton('Registrar datos')
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

        itembtn1 = types.KeyboardButton('Registrar datos')
        itembtn2 = types.KeyboardButton('Continuar con el registro actual')

        markup.row(itembtn1)
        markup.row(itembtn2)
    
        bot.send_message(message.chat.id, "Este número de documento ya existe en el sistema, ¿te gustaría continuar el registro del vehículo con los datos almacenados o te gustaría realizar un nuevo registro ?", reply_markup=markup)

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

    def validarDocumentoPropietario(message):
        #Validar si el documento del propietario ya existe, si ya existe se le pregunta al usuario si desea seguir con los datos ya existente o si desea continuar con un registro nuevo de usuario diferente
        existeVehiculo = Vehiculo.validarExistenciaDocumento(message)
        if existeVehiculo == True:
            Vehiculo.validarOpcionDeRegistro(bot, types, message)
        else:
            Vehiculo.solicitarCorreoElectronicoPropietario(message)

    def solicitarCorreoElectronicoPropietario(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta = Vehiculo.solicitarCorreoElectronico(message, bot)     

            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, Vehiculo.solicitarNombrePropietario)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")

    def solicitarNombrePropietario(message):
        try:

            if Vehiculo.validarExistenciaCorreoElectronico(message):
                Vehiculo.mostrarMenuPrincipal(message, bot, types, "No se puede realizar el registro debido a que el correo ya existe en el sistema, selecciona una opción:")
            else:
                #Persiste la respuesta ingresada por el usuario y retorna la respuesta
                respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor el nombre del propietario del vehículo', 'correoPropietario')
                
                #Se llama al metodo register_next_step_handler para continuar con la conversación 
                bot.register_next_step_handler(respuesta, Vehiculo.solicitarPlacaVehiculo)


        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")

    def solicitarPlacaVehiculo(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor la placa del vehículo', 'nombrePropietario')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, Vehiculo.solicitarDescripcionVehiculo)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")

    def solicitarDescripcionVehiculo(message):
        try:

            #Validar si la placa del vehiculo que se quiere registrar, ya existe en el sistema
            if(Vehiculo.validarExistenciaPlaca(message)):
                Vehiculo.mostrarMenuPrincipal(message, bot, types, "No se puede realizar el registro debido a que la placa ya existe en el sistema, selecciona una opción:")
            else:
                #Persiste la respuesta ingresada por el usuario y retorna la respuesta
                respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor la descripción del vehículo', 'placaVehiculo')
                
                #Se llama al metodo register_next_step_handler para continuar con la conversación 
                bot.register_next_step_handler(respuesta, Vehiculo.solicitarNivelAceiteVehiculo)

        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")   

    def solicitarNivelAceiteVehiculo(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor el nivel de aceite del vehículo', 'descripcioVehiculo')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, Vehiculo.solicitarNivelLiquidoVehiculo)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")   

    def solicitarNivelLiquidoVehiculo(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor el nivel de líquido del vehículo', 'nivelAceite')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, Vehiculo.solicitarNivelRefrigeranteVehiculo)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")  

    def solicitarNivelRefrigeranteVehiculo(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor el nivel de refrigerante del vehículo', 'nivelLiquidoFrenos')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, Vehiculo.solicitarNivelLiquidoDireccionVehiculo)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}") 

    def solicitarNivelLiquidoDireccionVehiculo(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor el nivel de líquido de dirección del vehículo', 'nivelRefrigerante')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, Vehiculo.solicitarFotoSoatVehiculo)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")  

    def solicitarFotoSoatVehiculo(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor el código del soat del vehículo', 'nivelLiquidoDireccion')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, Vehiculo.solicitarFotoSegurocontractualVehiculo)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")  

    def solicitarFotoSegurocontractualVehiculo(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor el código del seguro contractual del vehículo', 'soat')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, Vehiculo.solicitarFotoSeguroExtracontractualVehiculo)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")
    
    def solicitarFotoSeguroExtracontractualVehiculo(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor el código del seguro extracontractual del vehículo', 'seguroContractual')

            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, Vehiculo.almacenarDatosDeVehiculo)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")  

    def almacenarDatosDeVehiculo(message):
        try:

            #almacenar respuesta tota, en la base de datos
            Vehiculo.almacenarDatosVehiculo(message, bot)
            
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")


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

