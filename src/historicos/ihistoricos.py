from abc import ABC, abstractmethod
class Ihistorico(ABC):
    
    @abstractmethod
    def obtenerVehiculos(self):
        pass

    @abstractmethod
    def obtenerLiqudisoRepuestos(self):
        pass