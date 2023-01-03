#########################################################
from config import bot
from telebot import types
from time import sleep
from vehiculo.registrarDatosVehiculo import Vehiculo
######################################################### sqlalquemy

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)
# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

@bot.message_handler(commands=['start'])
def manejarMenuPrincipal(message):
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
    
    bot.send_message(message.chat.id, "Selecciona una opción del menú:", reply_markup=markup)

@bot.message_handler(regexp="Registrar datos de vehiculo")
def solicitarDocumentoPropietario(message):    
    respuesta = bot.send_message(message.chat.id, 'Ingresa por favor el documento del propietario del vehículo')
    bot.register_next_step_handler(respuesta, solicitarCorreoElectronicoPropietario)

def solicitarCorreoElectronicoPropietario(message):
    try:
        #Persiste la respuesta ingresada por el usuario y retorna la respuesta
        respuesta = Vehiculo.solicitarCorreoElectronico(message, bot)     

        #Se llama al metodo register_next_step_handler para continuar con la conversación 
        bot.register_next_step_handler(respuesta, solicitarNombrePropietario)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

def solicitarNombrePropietario(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor el nombre del propietario del vehículo', 'correoPropietario')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, solicitarPlacaVehiculo)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")

def solicitarPlacaVehiculo(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor la placa del vehículo', 'placaVehiculo')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, solicitarDescripcionVehiculo)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")

def solicitarDescripcionVehiculo(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor la descripción del vehículo', 'descripcioVehiculo')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, solicitarNivelAceiteVehiculo)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")   

def solicitarNivelAceiteVehiculo(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor el nivel de aceite del vehículo', 'nivelAceite')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, solicitarNivelLiquidoVehiculo)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")     

def solicitarNivelLiquidoVehiculo(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor el nivel de líquido del vehículo', 'nivelLiquidoFrenos')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, solicitarNivelRefrigeranteVehiculo)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")        

def solicitarNivelRefrigeranteVehiculo(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor el nivel de refrigerante del vehículo', 'nivelRefrigerante')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, solicitarNivelLiquidoDireccionVehiculo)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}") 

def solicitarNivelLiquidoDireccionVehiculo(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor el nivel de líquido de dirección del vehículo', 'nivelLiquidoDireccion')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, solicitarFotoSoatVehiculo)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")  

def solicitarFotoSoatVehiculo(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor la foto del soat del vehículo', 'soat')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, solicitarFotoSegurocontractualVehiculo)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")   

def solicitarFotoSegurocontractualVehiculo(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor la foto del seguro contractual del vehículo', 'seguroContractual')
            
            #Se llama al metodo register_next_step_handler para continuar con la conversación 
            bot.register_next_step_handler(respuesta, solicitarFotoSeguroExtracontractualVehiculo)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")    

def solicitarFotoSeguroExtracontractualVehiculo(message):
        try:
            #Persiste la respuesta ingresada por el usuario y retorna la respuesta
            respuesta =  Vehiculo.solicitarDatos(message, bot, 'Ingresa por favor la foto del seguro extracontractual del vehículo', 'seguroExtraContrActual')

            #almacenar respuesta tota, en la base de datos
            Vehiculo.almacenarDatosVehiculo(respuesta, message)

            bot.reply_to(message, 'Registro exitoso')
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")     
                                                                       


@bot.message_handler(regexp="Registrar líquidos y repuestos")
def manejarRegistroLiquidosRepuestos(message):
    bot.send_message(message.chat.id, 'Registrar líquidos y repuestos')

@bot.message_handler(regexp="Históricos")
def manejarHistoricos(message):
    bot.send_message(message.chat.id, 'Históricos')

@bot.message_handler(regexp="Seguros")
def manejarSeguros(message):
    bot.send_message(message.chat.id, 'Seguros')            


@bot.message_handler(func=lambda message: True)
def fallback(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    bot.reply_to(
        message,
        "\U0001F63F Ups, no entendí lo que me dijiste.")

#########################################################
if __name__ == '__main__':
    bot.polling(timeout=20)
#########################################################