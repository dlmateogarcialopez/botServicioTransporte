from liquidosRepuestos.registrarLiquidosRepuestos import LiqudosRepuestos
from time import sleep
import json
import os
import sys
#from vehiculo.registrarDatosVehiculo import vehiculos_registrados
from database.persistencia import vehiculos_registrados
from telebot import types
from config import bot
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from liquidosRepuestos.liquidosRepuestosDb import LiquidosRepuestoDb
from liquidosRepuestos.implementaciones import LectorFuenteDatos