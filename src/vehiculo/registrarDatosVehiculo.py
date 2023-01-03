class Record:
    def __init__(self):
        self.documentoPopietario = None
        self.correoPropietario = None
        self.nombrePropietario = None
        self.placaVehiculo = None
        self.descripcioVehiculo = None
        self.nivelAceite = None
        self.nivelLiquidoFrenos = None
        self.nivelRefrigerante = None
        self.nivelLiquidoDireccion = None
        self.soat = None
        self.seguroContractual = None
        self.seguroExtraContrActual = None


informacion_vehiculo = {}
class Vehiculo:

    def __init__(self):
        ...


    def solicitarCorreoElectronico(data, bot):

        record = Record()

        documentoPopietario = data.text
    
        record.documentoPopietario = documentoPopietario

        informacion_vehiculo[data.chat.id] = record

        respuesta = bot.reply_to(data, 'Ingresa por favor el correo electrónico del propietario del vehículo')

        return respuesta

    def obtenerClaveObjeto(record, clave, data):
        if clave == 'correoPropietario':
            record.correoPropietario = data.text
        elif clave == 'nombrePropietario':
            record.nombrePropietario = data.text
        elif clave == 'placaVehiculo':
            record.placaVehiculo = data.text       
        elif clave == 'descripcioVehiculo':
            record.descripcioVehiculo = data.text   
        elif clave == 'nivelAceite':
            record.nivelAceite = data.text  
        elif clave == 'nivelLiquidoFrenos':
            record.nivelLiquidoFrenos = data.text   
        elif clave == 'nivelRefrigerante':
            record.nivelRefrigerante = data.text      
        elif clave == 'nivelLiquidoDireccion':
            record.nivelLiquidoDireccion = data.text 
        elif clave == 'soat':
            record.soat = data.text      
        elif clave == 'seguroContractual':
            record.seguroContractual = data.text      
        elif clave == 'seguroExtraContrActual':
            record.seguroExtraContrActual = data.text

    def solicitarDatos(data, bot, mensaje, clave):        

        record = informacion_vehiculo[data.chat.id]

        Vehiculo.obtenerClaveObjeto(record, clave, data)
        
        respuesta = bot.reply_to(data, mensaje)

        return respuesta
                                                                                       

    def almacenarDatosVehiculo(respuesta, data):

        fotoSeguroExtraContractual = data.text

        record = informacion_vehiculo[data.chat.id]
        record.seguroExtraContrActual = fotoSeguroExtraContractual
    


    