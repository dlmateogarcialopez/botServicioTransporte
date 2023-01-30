from time import sleep
import json
import os
import sys
#from vehiculo.registrarDatosVehiculo import vehiculos_registrados
#from database.persistencia import vehiculos_registrados
#from liquidosRepuestos.registrarLiquidosRepuestos import informacion_liquidoRepuestos_registrados
#from database.persistencia import informacion_liquidoRepuestos_registrados
from telebot import types
from config import bot
from historicos.implementaciones import LectorFuenteDatos
from historicos.historicosDb import HistoricoDb

lista_placas = []
mi_path = "placas.txt"
placa_actual = {'placa':'sinPlaca'}
historicosDb = HistoricoDb(LectorFuenteDatos())


class ConsultarHistorico:

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

    # def validarExistenciaPlaca(data):
    #     lista_placas.clear()
    #     ConsultarHistorico.traerListaVehiculos()
    #     placa_upper = data.text.upper()
    #     if placa_upper in lista_placas:
    #         return True
    #     else:
    #         return False  

    def validarExistenciaPlaca(data):
        vehiculos = historicosDb.consultarVehiculos()
        for vehiculo in vehiculos:
            if vehiculo.placa == data.text:
                return True
        return False      


    def solicitarCedulaMecanicoPopietarioLiquidos(data, bot):

        placaVehiculo = data.text
        placa_actual['placa'] = placaVehiculo
    
        ConsultarHistorico.enviarAccionEscribiendo(data, bot)

        respuesta = bot.send_message(data.chat.id, 'Ingresa por favor el documento del propietario o mécanico asignado al vehículo')
        bot.register_next_step_handler(respuesta, ConsultarHistorico.validarMecanicoPropietarioPlacaLiquidos)


    def validarMecanicoPropietarioPlacaLiquidos(data):
        vehiculos = historicosDb.consultarVehiculos()
        if len(vehiculos) > 0:           
            for vehiculo in vehiculos:
                if vehiculo.placa == placa_actual['placa'] and (vehiculo.mecanicoAsignado == data.text or vehiculo.documentoPropietario == data.text):
                    placa_actual['placa'] = 'sinPlaca'
                    
                    #se muestra la información de la consulta
                    consulta = ""
                    liquidosRepuestos = historicosDb.obtenerLiqudisoRepuestos()
                    if len(liquidosRepuestos) > 0: 
                        for registro in liquidosRepuestos:
                            if registro.placa == vehiculo.placa:
                                consulta += f" \nNivel de aceite: {registro.nivelAceite} \nNivel Líquido de frenos: {registro.nivelLiquidoFrenos} \nNivel líquido refrigerante:  {registro.nivelRefrigerante} \nNivel líquido de dirección: {registro.nivelLiquidoDireccion} \n------------------------"
                    else: 
                        consulta= "No existe un histórico de registro de líquidos para el vehículo consultado"

                    bot.send_message(data.chat.id, f"El historial de líquidos registrados para el vehículo con placas {vehiculo.placa} es: {consulta} ")

                    ConsultarHistorico.mostrarMenuPrincipal(data, bot, types, "Muchas gracias, selecciona una opción:")
                    return                
            ConsultarHistorico.mostrarMenuPrincipal(data, bot, types, "No se puede realizar la consulta de líquidos debido a que el mecánico o el propietario ingresado no tiene asignado el vehículo, selecciona una opción:")            
        else:
            ConsultarHistorico.mostrarMenuPrincipal(data, bot, types, "No se encontró ningún vehículo, selecciona una opción:")  

    def solicitarCedulaMecanicoPopietarioRepuestos(data, bot):

        placaVehiculo = data.text
        placa_actual['placa'] = placaVehiculo
    
        ConsultarHistorico.enviarAccionEscribiendo(data, bot)

        respuesta = bot.send_message(data.chat.id, 'Ingresa por favor el documento del propietario o mécanico asignado al vehículo')
        bot.register_next_step_handler(respuesta, ConsultarHistorico.validarMecanicoPropietarioPlacaRepuestos)


    def validarMecanicoPropietarioPlacaRepuestos(data):
        vehiculos = historicosDb.consultarVehiculos()
        if len(vehiculos) > 0:           
            for vehiculo in vehiculos:
                if vehiculo.placa == placa_actual['placa'] and (vehiculo.mecanicoAsignado == data.text or vehiculo.documentoPropietario == data.text):
                    placa_actual['placa'] = 'sinPlaca'
                    
                    #se muestra la información de la consulta
                    consulta = ""
                    liquidosRepuestos = historicosDb.obtenerLiqudisoRepuestos()
                    if len(liquidosRepuestos) > 0: 
                        for registro in liquidosRepuestos:
                            if (registro.repuestos) != "":
                                if registro.placa == vehiculo.placa:
                                    consulta += f" \nCambio de repuestos : {registro.repuestos} \n------------------------"
                    else: 
                        consulta= "No existe un histórico de cambio de repuestos para el vehículo consultado"

                    bot.send_message(data.chat.id, f"El historial de repuestos registrados para el vehículo con placas {vehiculo.placa} es: {consulta} ")

                    ConsultarHistorico.mostrarMenuPrincipal(data, bot, types, "Muchas gracias, selecciona una opción:")
                    return                                   
            ConsultarHistorico.mostrarMenuPrincipal(data, bot, types, "No se puede realizar la consulta de repuestos debido a que el mecanico o el propietario ingresado no tiene asignado el vehículo, selecciona una opción:")            
        else:
            ConsultarHistorico.mostrarMenuPrincipal(data, bot, types, "No se encontró ningún vehículo, selecciona una opción:")  
