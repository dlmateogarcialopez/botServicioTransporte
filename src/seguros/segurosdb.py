from seguros.iseguro import Iseguro
class SeguroDb:
    def __init__(self, iseguro: Iseguro):
        self.iseguro = iseguro
    
    def consultarSeguro(self, placaVehiculo, documento):
        return self.iseguro.consultarSeguro(placaVehiculo, documento)

    def consultarSeguros(self):
        return self.iseguro.consultarSeguros()
    
    def actualizarSeguros(self, placa, soat, seguroContractual, seguroExtraContractual):
        return self.iseguro.actualizarSeguros(placa, soat, seguroContractual, seguroExtraContractual)
