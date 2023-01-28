from time import sleep
import json
import os
import sys
#from vehiculo.registrarDatosVehiculo import vehiculos_registrados
#from database.persistencia import vehiculos_registrados
#from liquidosRepuestos.registrarLiquidosRepuestos import informacion_liquidoRepuestos_registrados
from database.persistencia import informacion_liquidoRepuestos_registrados
from telebot import types
from config import bot
from historicos.implementaciones import LectorFuenteDatos
from historicos.historicosDb import HistoricoDb

lista_placas = []
placa_actual = {'placa':'sinPlaca'}
historicosDb = HistoricoDb(LectorFuenteDatos())


class ConsultarHistorico:

    def __init__(self):        
        ...

    def traerListaVehiculos():
        mi_path = "placas.txt"
        file_mode = "r"
        with open(mi_path, file_mode) as archivo:
            for linea in archivo:
                linea_limpia = linea.rstrip('\n')
                lista_placas.append(linea_limpia)
        
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
        
            bot.send_message(data.chat.id, msg, reply_markup=markup)  
    
    def enviarAccionEscribiendo(data, bot):
            bot.send_chat_action(data.chat.id, 'typing')
            sleep(1)    

    def validarExistenciaPlaca(data):
        lista_placas.clear()
        ConsultarHistorico.traerListaVehiculos()
        placa_upper = data.text.upper()
        return True if placa_upper in lista_placas else False


    def solicitarCedulaMecanicoPopietarioLiquidos(data, bot):

        placaVehiculo = data.text.upper()
        placa_actual['placa'] = placaVehiculo
    
        ConsultarHistorico.enviarAccionEscribiendo(data, bot)

        respuesta = bot.send_message(data.chat.id, 'Ingresa por favor el documento del propietario o mécanico asignado al vehículo')
        bot.register_next_step_handler(respuesta, ConsultarHistorico.validarMecanicoPropietarioPlacaLiquidos)


    def validarMecanicoPropietarioPlacaLiquidos(data):
        vehiculos = historicosDb.consultarVehiculos()
        if len(vehiculos) > 0:           
            for vehiculo in vehiculos:
                if vehiculo.placaVehiculo.upper() == placa_actual['placa'] and (vehiculo.mecanicoAsignado == data.text or vehiculo.documentoPopietario == data.text):
                    placa_actual['placa'] = 'sinPlaca'
                    
                    #se muestra la información de la consulta
                    consulta = ""
                    liquidosRepuestos = historicosDb.guardarLiquidosRepuestos()
                    if liquidosRepuestos: 
                        for registro in liquidosRepuestos:
                            consulta += f" \nNivel de aceite: {registro.nivelAceite} \nNivel Líquido de frenos: {registro.nivelLiquidoFrenos} \nNivel líquido refrigerante:  {registro.nivelRefrigerante} \nNivel líquido de dirección: {registro.nivelLiquidoDireccion} \n------------------------"
                    else: 
                        consulta= "No existe un histórico de registro de líquidos para el vehículo consultado"

                    bot.send_message(data.chat.id, f"El historial de líquidos registrados para el vehículo con placas {vehiculo.placaVehiculo} es: {consulta} ")

                    ConsultarHistorico.mostrarMenuPrincipal(data, bot, types, "Muchas gracias, selecciona una opción:")
                    return                
            ConsultarHistorico.mostrarMenuPrincipal(data, bot, types, "No se puede realizar la consulta de líquidos debido a que el mecánico o el propietario ingresado no tiene asignado el vehículo, selecciona una opción:")            
        else:
            ConsultarHistorico.mostrarMenuPrincipal(data, bot, types, "No se encontró ningún vehículo, selecciona una opción:")  

    def solicitarCedulaMecanicoPopietarioRepuestos(data, bot):

        placaVehiculo = data.text.upper()
        placa_actual['placa'] = placaVehiculo
    
        ConsultarHistorico.enviarAccionEscribiendo(data, bot)

        respuesta = bot.send_message(data.chat.id, 'Ingresa por favor el documento del propietario o mécanico asignado al vehículo')
        bot.register_next_step_handler(respuesta, ConsultarHistorico.validarMecanicoPropietarioPlacaRepuestos)


    def validarMecanicoPropietarioPlacaRepuestos(data):
        vehiculos = historicosDb.consultarVehiculos()
        if len(vehiculos) > 0:           
            for vehiculo in vehiculos:
                if vehiculo.placaVehiculo.upper() == placa_actual['placa'] and (vehiculo.mecanicoAsignado == data.text or vehiculo.documentoPopietario == data.text):
                    placa_actual['placa'] = 'sinPlaca'
                    
                    #se muestra la información de la consulta
                    consulta = ""
                    liquidosRepuestos = historicosDb.guardarLiquidosRepuestos()
                    if len(liquidosRepuestos) > 0: 
                        for registro in liquidosRepuestos:
                            if (registro.cambioRepuestos) != "":
                                consulta += f" \nCambio de repuestos : {registro.cambioRepuestos} \n------------------------"
                    else: 
                        consulta= "No existe un histórico de cambio de repuestos para el vehículo consultado"

                    bot.send_message(data.chat.id, f"El historial de repuestos registrados para el vehículo con placas {vehiculo.placaVehiculo} es: {consulta} ")

                    ConsultarHistorico.mostrarMenuPrincipal(data, bot, types, "Muchas gracias, selecciona una opción:")
                    return                                   
            ConsultarHistorico.mostrarMenuPrincipal(data, bot, types, "No se puede realizar la consulta de repuestos debido a que el mecanico o el propietario ingresado no tiene asignado el vehículo, selecciona una opción:")            
        else:
            ConsultarHistorico.mostrarMenuPrincipal(data, bot, types, "No se encontró ningún vehículo, selecciona una opción:")  
