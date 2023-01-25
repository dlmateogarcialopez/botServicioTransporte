from abc import ABC, abstractmethod
class Iseguro(ABC):
    @abstractmethod
    def consultarSeguro(self, placaVehiculo, documento) :
        pass

    @abstractmethod
    def consultarSeguros(self) :
        pass