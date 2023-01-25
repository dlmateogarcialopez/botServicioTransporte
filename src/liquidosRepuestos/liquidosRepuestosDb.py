from liquidosRepuestos.iliquidosRepuestos import ILquidoRepuesto

class LiquidosRepuestoDb():

    def __init__(self, iLiquidoRepuesto: ILquidoRepuesto):
        self.iLiquidoRepuesto = iLiquidoRepuesto

    def consultarVehiculos(self):
        return self.iLiquidoRepuesto.consultarVehiculos()

    def guardarLiquidosRepuestos(self, informacionLiquidosRepuestos):
        return self.iLiquidoRepuesto.guardarLiquidosRepuestos(informacionLiquidosRepuestos)
