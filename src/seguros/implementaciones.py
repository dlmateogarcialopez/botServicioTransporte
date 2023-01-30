from seguros.iseguro import Iseguro
#from database.persistencia import vehiculos_registrados
#from vehiculo.registrarDatosVehiculo import vehiculos_registrados
import database.db as db
class LectorFuenteDatos(Iseguro):    
    def consultarSeguro(self, placaVehiculo, documento) :

        vehiculos = db.session.query(db.Vehiculo).all()
        db.session.commit()

        for vehiculo in vehiculos:     
            if vehiculo.placa == placaVehiculo and (vehiculo.mecanicoAsignado == documento or vehiculo.documentoPropietario == documento):
                return vehiculo
            
        return False

    def consultarSeguros(self) :
        vehiculos = db.session.query(db.Vehiculo).all()
        db.session.commit()
        #return vehiculos_registrados
        return vehiculos
    
    def actualizarSeguros(self, placa, soat, seguroContractual, seguroExtraContractual):
        vehiculo = db.session.query(db.Vehiculo).get(placa)
        db.session.commit()

        vehiculo.soat = soat
        vehiculo.seguroContractual = seguroContractual
        vehiculo.seguroExtraContractual = seguroExtraContractual
        db.session.commit()

        return True