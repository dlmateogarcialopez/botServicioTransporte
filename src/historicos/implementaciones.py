from historicos.ihistoricos import Ihistorico
from database.persistencia import vehiculos_registrados
from database.persistencia import informacion_liquidoRepuestos_registrados

class LectorFuenteDatos(Ihistorico):

    def obtenerVehiculos(self):
        return vehiculos_registrados
    
    
    def obtenerLiqudisoRepuestos(self):
        return informacion_liquidoRepuestos_registrados
