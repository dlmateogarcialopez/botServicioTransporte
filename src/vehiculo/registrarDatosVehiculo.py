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
                                                                                       

    def almacenarDatosVehiculo(data):

        fotoSeguroExtraContractual = data.text

        record = informacion_vehiculo[data.chat.id]
        record.seguroExtraContrActual = fotoSeguroExtraContractual


    def validarExistenciaDocumento(data):
        if data.text == '123':

            record = Record()

            informacion_vehiculo[data.chat.id] = record

            datosVehiculo = informacion_vehiculo[data.chat.id]
            datosVehiculo.documentoPopietario = data.text
            datosVehiculo.correoPropietario = "correo@gmail.com"
            datosVehiculo.nombrePropietario = "Nombre existente"

            return True
        else:
            return False

    def validarOpcionDeRegistro(bot, types, message):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

        itembtn1 = types.KeyboardButton('Registrar datos de vehiculo')
        itembtn2 = types.KeyboardButton('Continuar con el registro actual')

        markup.row(itembtn1)
        markup.row(itembtn2)
    
        bot.send_message(message.chat.id, "Este número de documento ya existe en el sistema, ¿te gustaría continuar el registro del vehículo con un los datos almacenados o te gustaría realizar un nuevo registro ?:", reply_markup=markup)

    