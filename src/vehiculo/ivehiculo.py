from abc import ABC, abstractmethod
class Ivehiculo(ABC):
    @abstractmethod
    def guardarVehiculo(self, vehiculo):
        pass

    @abstractmethod
    def consultarVehiculos(self, vehiculo):
        pass