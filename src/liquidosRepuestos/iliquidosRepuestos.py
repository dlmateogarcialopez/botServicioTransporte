from abc import ABC, abstractmethod
class ILquidoRepuesto ( ABC ) :
    
    @abstractmethod
    def consultarVehiculos(self) :
        pass

    @abstractmethod
    def guardarLiquidosRepuestos(self, informacionLiquidosRepuestos):
        pass