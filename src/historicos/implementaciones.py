from historicos.ihistoricos import Ihistorico
from database.persistencia import vehiculos_registrados
from database.persistencia import informacion_liquidoRepuestos_registrados
import database.db as db

class LectorFuenteDatos(Ihistorico):

    def obtenerVehiculos(self):
        #return vehiculos_registrados
        vehiculos = db.session.query(db.Vehiculo).all()
        db.session.commit()
        return vehiculos
    
    
    def obtenerLiqudisoRepuestos(self):
        #return informacion_liquidoRepuestos_registrados
        liquidos = db.session.query(db.LiquidoRepuesto).all()
        db.session.commit()
        return liquidos
