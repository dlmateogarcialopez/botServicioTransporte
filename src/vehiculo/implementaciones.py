#from database.persistencia import vehiculos_registrados
from vehiculo.ivehiculo import Ivehiculo
import database.db as db
from database.db import Vehiculo
from datetime import datetime

class LectorFuenteDatos(Ivehiculo):

    def __init__(self) -> None:
        super().__init__()

    def guardarVehiculo(self, vehiculo):
        #vehiculos_registrados.append(vehiculo)
        account = Vehiculo(vehiculo.placaVehiculo, vehiculo.documentoPopietario, vehiculo.correoPropietario, vehiculo.nombrePropietario, vehiculo.descripcioVehiculo, vehiculo.nivelAceite, vehiculo.nivelLiquidoFrenos, vehiculo.nivelRefrigerante, vehiculo.nivelLiquidoDireccion, vehiculo.soat, vehiculo.seguroContractual, vehiculo.seguroExtraContrActual, vehiculo.mecanicoAsignado, datetime.now())
        db.session.add(account)
        db.session.commit()
        

    def consultarVehiculos(self):
        vehiculos = db.session.query(Vehiculo).all()
        db.session.commit()
        #return vehiculos_registrados
        return vehiculos