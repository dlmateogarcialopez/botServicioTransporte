from vehiculo.ivehiculo import Ivehiculo
class VehiculoDb :
    def __init__(self, ivehiculo: Ivehiculo):
        self.ivehiculo = ivehiculo

    def guardarVehiculo(self, vehiculo):
        self.ivehiculo.guardarVehiculo(vehiculo)
    
    def consultarVehiculos(self):
        return self.ivehiculo.consultarVehiculos()
