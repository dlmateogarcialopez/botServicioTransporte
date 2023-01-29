from database.persistencia import vehiculos_registrados
from vehiculo.ivehiculo import Ivehiculo
import database.db as db
from database.db import Mecanico
from datetime import datetime

class LectorFuenteDatos(Ivehiculo):

    def __init__(self) -> None:
        super().__init__()

    def guardarVehiculo(self, vehiculo):
        vehiculos_registrados.append(vehiculo)
        #account = Mecanico('10', 'juan', True, 'hqd69f', datetime.now())
        #db.session.add(account)
        #db.session.commit()
        

    def consultarVehiculos(self):
        return vehiculos_registrados