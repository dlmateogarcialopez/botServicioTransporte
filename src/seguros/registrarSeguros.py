#from vehiculo.registrarDatosVehiculo import vehiculos_registrados
#from database.persistencia import vehiculos_registrados
from telebot import types
from config import bot
from seguros.segurosdb import SeguroDb
from seguros.implementaciones import LectorFuenteDatos
placa = {'placa':'sinPlaca'}
placaConsulta = {'placa':'sinPlaca'}
seguros = {}
segurooDb = SeguroDb(LectorFuenteDatos())
class Seguro:
    def __init__(self):
        ...        

    def validarPlacaVehiculoRegistro(message):
        try:
            existeVehiculo = 0
            vehiculos = segurooDb.consultarSeguros()
            for vehiculo in vehiculos:     
                if vehiculo.placaVehiculo == message.text:
                    placa['placa'] = vehiculo.placaVehiculo
                    existeVehiculo = existeVehiculo + 1

            #Validar si la placa existe, en caso de que si exista, se continúa con el registro, de lo contrario no se seguirá con el registro y se mostrará el menú principal
            if existeVehiculo > 0:
                respuesta = bot.send_message(message.chat.id, 'Ingresa por favor el SOAT')
                bot.register_next_step_handler(respuesta, Seguro.almacenarSoat)
            else:
                Seguro.mostrarMenuPrincipal(message, bot, types, "No se encontró un vehículo con la placa ingresada, selecciona una opción:")
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")                            

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
        
            bot.send_message(data.chat.id, msg, reply_markup=markup)    

    def almacenarSoat(message):
        try:

            #Almacenar temporalmente el soat en el diccionario
            seguros['soat'] = message.text

            #Respuesta al usuario        
            respuesta = bot.send_message(message.chat.id, 'Ingresa por favor el seguro contractual')
            bot.register_next_step_handler(respuesta, Seguro.almacenarSeguroContractual)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")   

    def almacenarSeguroContractual(message):
        try:
            #Almacenar temporalmente el seguro Contractual en el diccionario
            seguros['seguroContractual'] = message.text
            
            respuesta = bot.send_message(message.chat.id, 'Ingresa por favor el seguro extracontractual')
            bot.register_next_step_handler(respuesta, Seguro.almacenarSeguros)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")      

    def almacenarSeguros(message):
        try:

            #Almacenar temporalmente el seguro seguro extraContrActual en el diccionario
            seguros['seguroExtraContrActual'] = message.text

            #validar si el diccionario "seguros" esta completo, para poder realizar la actualización de los seguros
            if len(seguros) == 3:
                vehiculos = segurooDb.consultarSeguros()
                for carro in vehiculos:
                    if carro.placaVehiculo == placa['placa']:
                        carro.soat = seguros['soat']
                        carro.seguroContractual = seguros['seguroContractual']
                        carro.seguroExtraContrActual = seguros['seguroExtraContrActual']
                        placa['placa'] = 'sinPlaca'
                        break
            bot.reply_to(message, 'Registro exitoso de los seguros')
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")

        #Almacenar en un objeto los tres seguros y cuando se este seguro que se ingresaron los tres, se realiza la actualización                 
      
    #Validar si la placa está en el sistema para consultar el documento del propietario o mecánico
    def validarPlacaVehiculoConsulta(message):
        try:            
            vehiculos = segurooDb.consultarSeguros()
            if len(vehiculos) > 0:
                for vehiculo in vehiculos:     
                    if vehiculo.placaVehiculo == message.text:
                        placaConsulta['placa'] = message.text
                        respuesta = bot.send_message(message.chat.id, 'Ingresa por favor el documento del mecánico o del propietario')                        
                        bot.register_next_step_handler(respuesta, Seguro.validarDocumento)

                        return
                Seguro.mostrarMenuPrincipal(message, bot, types, "No se encontró un vehículo con la placa ingresada, selecciona una opción:")
            else:
                Seguro.mostrarMenuPrincipal(message, bot, types, "No se encontró un vehículo con la placa ingresada, selecciona una opción:")

        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")       

    def validarTerminaciónDeConversacion(message):
        try:
            if message.text == 'Si':
                Seguro.mostrarMenuPrincipal(message, bot, types, "Por favor selecciona una opción")
            elif message.text == 'No':
                bot.send_message(message.chat.id, f"Muchas gracias por usar mis servicios, espero que te vuelvas a contactar conmigo en futuras ocasiones")
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}") 

    def validarDocumento(message):
        vehiculos = segurooDb.consultarSeguros()
        if len(vehiculos) > 0:
            vehiculo = segurooDb.consultarSeguro(placaConsulta['placa'], message.text)
            if(vehiculo == False):
                Seguro.mostrarMenuPrincipal(message, bot, types, "No existe un vehículo con los datos proporcionados, selecciona una opción:")
            else:
                    placaConsulta['placa'] = 'sinPlaca'
                    #mensaje que se le envia a l usuario para mostrar la información de los seguros
                    bot.send_message(message.chat.id, f"Los últimos seguros registrados para el vehículo con placas {vehiculo.placaVehiculo} son: \nSOAT: {vehiculo.soat} \nSeguro contractual: {vehiculo.seguroContractual} \nSeguro extracontractual: {vehiculo.seguroExtraContrActual}")

                    #Mostrar opción de continuar con la charla  o terminar
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

                    itembtn1 = types.KeyboardButton('Si')
                    itembtn2 = types.KeyboardButton('No')

                    markup.row(itembtn1)
                    markup.row(itembtn2)
                    
                    respuesta = bot.send_message(message.chat.id, '¿Te puedo ayudar en algo más?', reply_markup=markup)  
                    bot.register_next_step_handler(respuesta, Seguro.validarTerminaciónDeConversacion)
                    return
        else:
            Seguro.mostrarMenuPrincipal(message, bot, types, "No se encontró un vehículo con la placa ingresada, selecciona una opción:")           