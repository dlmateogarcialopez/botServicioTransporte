from seguros.iseguro import Iseguro
from database.persistencia import vehiculos_registrados
#from vehiculo.registrarDatosVehiculo import vehiculos_registrados
class LectorFuenteDatos(Iseguro):    
    def consultarSeguro(self, placaVehiculo, documento) :
        for vehiculo in vehiculos_registrados:     
            if vehiculo.placaVehiculo == placaVehiculo and (vehiculo.mecanicoAsignado == documento or vehiculo.documentoPopietario == documento):
                return vehiculo
        return False


    def consultarSeguros(self) :
        return vehiculos_registrados 