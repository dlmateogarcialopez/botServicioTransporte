from database.persistencia import vehiculos_registrados
from vehiculo.ivehiculo import Ivehiculo
class LectorFuenteDatos(Ivehiculo):

    def guardarVehiculo(self, vehiculo):
        vehiculos_registrados.append(vehiculo)

    def consultarVehiculos(self):
        return vehiculos_registrados
