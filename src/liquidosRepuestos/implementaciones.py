from liquidosRepuestos.iliquidosRepuestos import ILquidoRepuesto
from database.persistencia import vehiculos_registrados
from database.persistencia import informacion_liquidoRepuestos_registrados
class LectorFuenteDatos(ILquidoRepuesto):
        def consultarVehiculos(self) :
            return vehiculos_registrados

        def guardarLiquidosRepuestos(self, informacionLiquidosRepuestos):
            informacion_liquidoRepuestos_registrados.append(informacionLiquidosRepuestos)