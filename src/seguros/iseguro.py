from abc import ABC, abstractmethod
class Iseguro(ABC):
    @abstractmethod
    def consultarSeguro(self, placaVehiculo, documento) :
        pass

    @abstractmethod
    def consultarSeguros(self) :
        pass

    @abstractmethod
    def actualizarSeguros(self, placa, soat, seguroContractual, seguroExtraContractual):
        pass
