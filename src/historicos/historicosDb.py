from historicos.ihistoricos import Ihistorico


class HistoricoDb():
    
    def __init__(self, ihistorico: Ihistorico):
        self.ihistorico = ihistorico


    def consultarVehiculos(self):
        return self.ihistorico.obtenerVehiculos()
    
    def obtenerLiqudisoRepuestos(self):
        return self.ihistorico.obtenerLiqudisoRepuestos()
