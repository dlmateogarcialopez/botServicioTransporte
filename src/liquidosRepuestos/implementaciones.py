from liquidosRepuestos.iliquidosRepuestos import ILquidoRepuesto
#from database.persistencia import vehiculos_registrados
from database.persistencia import informacion_liquidoRepuestos_registrados
import database.db as db
from datetime import datetime

class LectorFuenteDatos(ILquidoRepuesto):
        def consultarVehiculos(self) :
            #return vehiculos_registrados
            vehiculos = db.session.query(db.Vehiculo).all()
            db.session.commit()
            return vehiculos

        def guardarLiquidosRepuestos(self, informacionLiquidosRepuestos):
            #informacion_liquidoRepuestos_registrados.append(informacionLiquidosRepuestos)
            account = db.LiquidoRepuesto(informacionLiquidosRepuestos.placaVehiculo, informacionLiquidosRepuestos.nivelAceite, informacionLiquidosRepuestos.cedulaMecanico, informacionLiquidosRepuestos.nivelLiquidoFrenos, informacionLiquidosRepuestos.nivelRefrigerante, informacionLiquidosRepuestos.nivelLiquidoDireccion, informacionLiquidosRepuestos.cambioRepuestos, datetime.now())
            db.session.add(account)
            db.session.commit()
