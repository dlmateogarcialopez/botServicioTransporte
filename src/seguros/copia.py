from seguros.vehiculosRegistradosTmp import vehiculos_registrados
from telebot import types
from config import bot
placa = ''
seguros = {}
class Seguro:
    def __init__(self):
        ...

    def validarPlacaVehiculo(message):
        existeVehiculo = 0
        for vehiculo in vehiculos_registrados:     
            if vehiculos_registrados[vehiculo]['placaVehiculo'] == message.text:
                placa = vehiculos_registrados[vehiculo]['placaVehiculo']
                existeVehiculo = existeVehiculo + 1

        #Validar si la placa existe, en caso de que si exista, se continúa con el registro, de lo contrario no se seguirá con el registro y se mostrará el menú principal
        if existeVehiculo > 0:
            try:
                respuesta = bot.send_message(message.chat.id, 'Ingresa por favor el SOAT')
                bot.register_next_step_handler(respuesta, Seguro.almacenarSoat)
            except Exception as e:
                bot.reply_to(message, f"Algo terrible sucedió: {e}") 
        else:
            Seguro.mostrarMenuPrincipal(message, bot, types, "No se encontró un vehículo con la placa ingresada, selecciona una opción:")            

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
            
            respuesta = bot.send_message(message.chat.id, 'Ingresa por favor el seguro contractual')
            bot.register_next_step_handler(respuesta, Seguro.almacenarSeguroContraExtractual)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")      

    def almacenarSeguroContraExtractual(message):
        try:

            #Almacenar temporalmente el seguro seguro extraContrActual en el diccionario
            seguros['seguroExtraContrActual'] = message.text

            #validar si el diccionario "seguros" esta completo
            print(len(seguros))

            for carro in vehiculos_registrados:
                if vehiculos_registrados[carro]['placaVehiculo'] == placa:
                    vehiculos_registrados[carro]['soat'] = seguros['soat']
                    vehiculos_registrados[carro]['seguroContractual'] = seguros['seguroContractual']
                    vehiculos_registrados[carro]['seguroExtraContrActual'] = seguros['seguroExtraContrActual']
            
            bot.reply_to(message, 'Registro exitoso de los seguros')
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")     

        #Almacenar en un objeto los tres seguros y cuando se este seguro que se ingresaron los tres, se realiza la actualización                 
      

