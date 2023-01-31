import unittest
from liquidosRepuestos.registrarLiquidosRepuestos import LiqudosRepuestos
from liquidosRepuestos.registrarLiquidosRepuestos import Record
from test.data import data
from vehiculo.registrarDatosVehiculo import Vehiculo
from vehiculo.registrarDatosVehiculo import  Record as Record2
from database.persistencia import vehiculos_registrados
from vehiculo.vehiculoDb import VehiculoDb
class testLiquidos (unittest.TestCase):

    def setUp(self):
        self.liquidos = LiqudosRepuestos()
        self.informacion_liquidoRepuestos = {}
        self.informacion_vehiculo = {}
        self.record = Record()
        self.recordVehiculo = Record2()     

    """ ********************* IMPORTANTE **********************  """  
    """ PARA EJECUTAR LAS PRUEBAS SE DEBE DE PONER self  EN LA PRIMERA POSICIÓN DE LOS PARAMETROS DE LAS FUNCIONES A TESTEAR """    

    def test_existencia_placa(self):
        """prueba para validar que si existe registrada la placa dada"""

        self.data = data("fgdd", 545, "ffff", "sdfg", "kjuu", "OPQ147")
         
        resultado_validacion = self.liquidos.validarExistenciaPlaca(self.data)

        self.assertTrue(resultado_validacion)


    def test_no_existencia_placa(self):
        """prueba para validar que no existe registrada la placa dada"""

        self.data = data("fgdd", 545, "ffff", "sdfg", "kjuu", "ahu876")

        resultado_validacion = self.liquidos.validarExistenciaPlaca(self.data)

        self.assertFalse(resultado_validacion)

    def test_obtenerClaveObjeto_valido(self):
        """prueba para validar que el objeto del registro de líquidos y repuestos está guardando correctamente"""

        self.data = data("fgdd", 545, "ffff", "sdfg", "kjuu", "se cambió el freno delantero")

        self.record.placaVehiculo = "aht52g"
        self.informacion_liquidoRepuestos[self.data.id] = self.record

        record2 = self.informacion_liquidoRepuestos[self.data.id]
        clave = "cambioRepuestos"
        resultado = self.liquidos.obtenerClaveObjeto(record2 ,clave, self.data)

        self.assertEquals("se cambió el freno delantero", self.record.cambioRepuestos )
        
    def test_validar_datos_completos(self):
        """ prueba para validar que toda la información requerida, fue ingresada por el usuario para poderla ingresar a la DB """

        self.data = data("fgdd", 546, "ffff", "sdfg", "kjuu", "se cambió el freno delantero")

        self.record.placaVehiculo = "DFG56R"
        self.record.nivelAceite = "9"
        self.record.cedulaMecanico = "1053866958"
        self.record.nivelLiquidoFrenos = "10"
        self.record.nivelRefrigerante = "20"
        self.record.nivelLiquidoDireccion = "27"
        self.record.cambioRepuestos = "se cambió el freno delantero"

        self.informacion_liquidoRepuestos[self.data.id] = self.record

        record2 = self.informacion_liquidoRepuestos[self.data.id]

        resultado = self.liquidos.validarDatosCompletos(record2)

        self.assertTrue(resultado)

    def test_validar_datos_completos_sin_placaVehiculo(self):
        """ prueba para validar que falta algun valor que se necesita para ingresar el registro de líquidos a la DB """

        self.data = data("fgdd", 546, "ffff", "sdfg", "kjuu", "se cambió el freno delantero")

        self.record.nivelAceite = "9"
        self.record.cedulaMecanico = "1053866958"
        self.record.nivelLiquidoFrenos = "10"
        self.record.nivelRefrigerante = "20"
        self.record.nivelLiquidoDireccion = "27"
        self.record.cambioRepuestos = "se cambió el freno delantero"

        self.informacion_liquidoRepuestos[self.data.id] = self.record

        record2 = self.informacion_liquidoRepuestos[self.data.id]

        resultado = self.liquidos.validarDatosCompletos(record2)

        self.assertFalse(resultado)


    def test_validar_envio_correo(self):
        """ prueba para validar que se envíe el correo electrónico al propietario """

        self.data = data("fgdd", 0, "ffff", "sdfg", "kjuu", "se cambió el freno delantero")

        
        self.recordVehiculo.documentoPopietario = "1053866958"
        self.recordVehiculo.correoPropietario = "laulopez0204@gmail.com"
        self.recordVehiculo.nombrePropietario = "laura garcía"
        self.recordVehiculo.placaVehiculo = "QWERTY"
        self.recordVehiculo.descripcioVehiculo = "prueba vehículo"
        self.recordVehiculo.nivelAceite = "10"
        self.recordVehiculo.nivelLiquidoFrenos = "11"
        self.recordVehiculo.nivelRefrigerante = "12"
        self.recordVehiculo.nivelLiquidoDireccion = "13"
        self.recordVehiculo.soat = "8956666"
        self.recordVehiculo.seguroContractual = "852963"
        self.recordVehiculo.seguroExtraContrActual = "987456321"
        self.recordVehiculo.mecanicoAsignado = "123"
        
        vehiculos_registrados.append(self.recordVehiculo)
       
        resultado = self.liquidos.enviarCorreo(self.data)

        self.assertTrue(resultado)


        
