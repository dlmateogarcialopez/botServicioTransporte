#########################################################
from config import bot
from telebot import types
from time import sleep
from vehiculo.registrarDatosVehiculo import Vehiculo
from seguros.registrarSeguros import Seguro
from liquidosRepuestos.registrarLiquidosRepuestos import LiqudosRepuestos
from historicos.consultarHistoricos import ConsultarHistorico
import database.db as db
from datetime import datetime
#########################################################


#########################################################
if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)

    #MECANICO 1
    mecanico1 = db.session.query(db.Mecanico).get("10")
    db.session.commit()

    if mecanico1 == None:
        account1 = db.Mecanico('10', 'juan', True, 'hqd69f', datetime.now())
        db.session.add(account1)

    #MECANICO 1
    mecanico2 = db.session.query(db.Mecanico).get("11")
    db.session.commit()

    if mecanico1 == None: 
        account2 = db.Mecanico('11', 'mateo', False, 'hqd68f', datetime.now())
        db.session.add(account2)

    db.session.commit()  
#########################################################

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

    itembtn1 = types.KeyboardButton('Registrar datos')
    itembtn2 = types.KeyboardButton('Registrar líquidos y repuestos')
    itembtn3 = types.KeyboardButton('Históricos')
    itembtn4 = types.KeyboardButton('Seguros')

    markup.row(itembtn1)
    markup.row(itembtn2)
    markup.row(itembtn3)
    markup.row(itembtn4)
    #markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    
    bot.send_message(message.chat.id, "Selecciona una opción del menú:", reply_markup=markup)

@bot.message_handler(regexp="Registrar datos")
def solicitarDocumentoPropietario(message):
    respuesta = bot.send_message(message.chat.id, 'Ingresa por favor el documento del propietario del vehículo')
    bot.register_next_step_handler(respuesta, Vehiculo.validarDocumentoPropietario)


@bot.message_handler(regexp="Continuar con el registro actual")
def solicitarDocumentoPropietario(message): 
        Vehiculo.enviarAccionEscribiendo(message, bot)   
        placaVehiculo = bot.send_message(message.chat.id, 'Ingresa por favor la placa del vehículo')
        bot.register_next_step_handler(placaVehiculo, Vehiculo.solicitarDescripcionVehiculo)
          

## inicio código Laura ##

@bot.message_handler(regexp="Registrar líquidos y repuestos")
def manejarRegistroLiquidosRepuestos(message):
    LiqudosRepuestos.enviarAccionEscribiendo(message, bot)   
    respuesta = bot.send_message(message.chat.id, 'Ingresa por favor la placa del vehículo al cual le va a registrar líquidos y repuestos')

    #respuesta = LiqudosRepuestos.solicitarPlaca(message, bot)     
    bot.register_next_step_handler(respuesta, solicitarCedulaMecanico)
  
## fin código Laura ##

## inicio código Laura ##
def solicitarCedulaMecanico(message):
        try:
            #Validar si la placa ingresada, existe en el sistema
            if (LiqudosRepuestos.validarExistenciaPlaca(message)) == False:
                LiqudosRepuestos.mostrarMenuPrincipal(message, bot, types, "No se puede realizar el registro debido a que la placa no está en el sistema, selecciona una opción:")
            else:
                #Persiste la respuesta ingresada por el usuario y retorna la respuesta
                respuesta =  LiqudosRepuestos.solicitarCedulaMecanico(message, bot)
                
                #Se llama al metodo register_next_step_handler para continuar con la conversación 
                #bot.register_next_step_handler(respuesta, solicitarNivelAceite)

        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")  

## fin código Laura ##

## inicio código Laura ##

@bot.message_handler(regexp="Históricos")
def manejarHistoricos(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    itembtn1 = types.KeyboardButton('Histórico de líquidos')
    itembtn2 = types.KeyboardButton('Histórico de Repuestos')

    markup.row(itembtn1)
    markup.row(itembtn2)
    
    bot.send_message(message.chat.id, "Selecciona la opción del historico que desea:", reply_markup=markup)   

#Metodo para realizar la consulta del Histórico de líquidos
@bot.message_handler(regexp="Histórico de líquidos")
def historicoLiquidos(message):
        try:
            respuesta = bot.send_message(message.chat.id, 'Ingresa por favor la placa del vehículo a consultar')
            bot.register_next_step_handler(respuesta, solicitarCedulaMecanicoPropietarioLiquidos)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")   

#Metodo para realizar la consulta del Histórico de Repuestos
@bot.message_handler(regexp="Histórico de Repuestos")
def historicoRepuestos(message):
        try:
            respuesta = bot.send_message(message.chat.id, 'Ingresa por favor la placa del vehículo a consultar')
            bot.register_next_step_handler(respuesta, solicitarCedulaMecanicoPropietarioRepuestos)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")   


def solicitarCedulaMecanicoPropietarioLiquidos(message):
        try:
            #Validar si la placa ingresada, existe en el sistema
            if (ConsultarHistorico.validarExistenciaPlaca(message)) == False:
                ConsultarHistorico.mostrarMenuPrincipal(message, bot, types, "No se puede realizar la consulta debido a que la placa no está en el sistema, selecciona una opción:")
            else:
                #Persiste la respuesta ingresada por el usuario y retorna la respuesta
                respuesta =  ConsultarHistorico.solicitarCedulaMecanicoPopietarioLiquidos(message, bot)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")  

def solicitarCedulaMecanicoPropietarioRepuestos(message):
        try:
            #Validar si la placa ingresada, existe en el sistema
            if (ConsultarHistorico.validarExistenciaPlaca(message)) == False:
                ConsultarHistorico.mostrarMenuPrincipal(message, bot, types, "No se puede realizar la consulta debido a que la placa no está en el sistema, selecciona una opción:")
            else:
                #Persiste la respuesta ingresada por el usuario y retorna la respuesta
                respuesta =  ConsultarHistorico.solicitarCedulaMecanicoPopietarioRepuestos(message, bot)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")  


## fin código Laura ##

## inicio código Mateo ##
@bot.message_handler(regexp="Seguros")
def manejarSeguros(message):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

        itembtn1 = types.KeyboardButton('Registrar')
        itembtn2 = types.KeyboardButton('Consultar')

        markup.row(itembtn1)
        markup.row(itembtn2)
        #markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    
        bot.send_message(message.chat.id, "Selecciona una opción del menú de seguros:", reply_markup=markup)   

#Metodo para realizar el registro de los seguros
@bot.message_handler(regexp="Registrar")
def registrarSeguros(message):
        try:
            respuesta = bot.send_message(message.chat.id, 'Ingresa por favor la placa del vehículo')
            bot.register_next_step_handler(respuesta, Seguro.validarPlacaVehiculoRegistro)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")               
           
#Metodo para la consulta de los seguros
@bot.message_handler(regexp="Consultar")
def consultarSeguros(message):
        try:
            respuesta = bot.send_message(message.chat.id, 'Ingresa por favor la placa del vehículo')
            bot.register_next_step_handler(respuesta, Seguro.validarPlacaVehiculoConsulta)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}") 


@bot.message_handler(commands=['help'])
def mostrarAyuda(message):
     
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    response = (
                "Estos son los comandos y órdenes disponibles para este chat \U0000270D :\n"
                "\n"
                "*/start* - Inicia la interacción con el bot y se presentan las opciones disponibles, para seleccionar alguna\n"
                "*/help* - Muestra este mensaje de ayuda con alguna información sobre las funcionaes y manejo del chat\n"
                "*Registrar datos* - Permite registrar un nuevo vehículo a la base de datos con toda la información necesaria\n"
                "*Registrar líquidos y repuestos* - Permite registrar la revisión de líquidos y repuestos de cierto vehículo en específico\n"
                "*Históricos* - En esta opción se podra tener la opción de Históricos de líquidos (Se permite consultar el histrorial de líquidos registrados para cierto vehículo) e Histórico de repuestos (Se permite consultar el histrorial de repuestos registrados para cierto vehículo)\n"
                "*Seguros* - Permite actualizar la información de los tres seguros de algún vehículo registrado\n"
                "\U0001F4AF"
                )
    
    #\U0001F4AF
    bot.send_message(message.chat.id, response, parse_mode="Markdown")
                  


## fin código Mateo ##

@bot.message_handler(func=lambda message: True)
def fallback(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    Vehiculo.mostrarMenuPrincipal(message, bot, types, "\U0001F63F Ups, no entendí lo que me dijiste, por favor selecciona una opción")

#########################################################
if __name__ == '__main__':
    bot.polling(timeout=20)
#########################################################