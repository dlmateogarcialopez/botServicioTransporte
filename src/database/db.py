from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, DateTime, ForeignKey, func, Integer, Boolean
from sqlalchemy.orm import relationship

engine = create_engine (
 'sqlite:///database/vehiculos.sqlite',
  echo=True,
  connect_args = {'check_same_thread': False})
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Mecanico(Base):
    __tablename__ = 'mecanicos'
        
    documento = Column('documento', String(15), primary_key=True, nullable=False)
    nombre = Column('nombre', String(30), nullable=False)
    disponibilidad = Column('disponibilidad', Boolean, nullable=False)
    carroAsignado = Column('carroAsignado', String(20), nullable=False)
    fecha = Column('fecha', DateTime, server_default=func.now(), nullable=True)


    def __init__(self, documento, nombre, disponibilidad, carroAsignado, fecha):
        self.documento = documento
        self.nombre = nombre
        self.disponibilidad = disponibilidad
        self.carroAsignado = carroAsignado
        self.fecha = fecha

    def __repr__(self):
        return f"<mecanicos {self.documento}>"
    
# class Vehiculo(Base):
#     __tablename__ = 'vehiculos'

#     placa = Column('placa', String(20), primary_key=True)
#     documentoPropietario = Column('documentoPropietario', String(20), nullable=False)
#     correoPropietario = Column('correoPropietario', String(60), nullable=False)
#     nombrePropietario = Column('nombrePropietario', String(60), nullable=False)
#     descripcionVehiculo = Column('descripcionVehiculo', String(200), nullable=False)
#     nivelAceite = Column('nivelAceite', String(10), nullable=False)
#     nivelLiquidoFrenos = Column('nivelLiquidoFrenos', String(10), nullable=False)
#     nivelRefrigerante = Column('nivelRefrigerante', String(10), nullable=False)
#     nivelLiquidoDireccion = Column('nivelLiquidoDireccion', String(10), nullable=False)
#     soat = Column('soat', String(10), nullable=False)
#     seguroContractual = Column('seguroContractual', String(10), nullable=False)
#     seguroExtraContractual = Column('seguroExtraContractual', String(10), nullable=False)
#     mecanicoAsignado = Column('mecanicoAsignado', String(15), ForeignKey('mecanicos.documento', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
#     mecanico = relationship("Mecanico")
#     fecha = Column('fecha', DateTime, server_default=func.now(), nullable=True)

#     def __init__(self, placa, documentoPropietario, correoPropietario, nombrePropietario, descripcionVehiculo, nivelAceite, nivelLiquidoFrenos, nivelRefrigerante, nivelLiquidoDireccion, soat, seguroContractual, seguroExtraContractual, mecanicoAsignado, fecha):
#         self.placa = placa
#         self.documentoPropietario = documentoPropietario
#         self.correoPropietario = correoPropietario
#         self.nombrePropietario = nombrePropietario
#         self.descripcionVehiculo = descripcionVehiculo
#         self.nivelAceite = nivelAceite
#         self.nivelLiquidoFrenos = nivelLiquidoFrenos
#         self.nivelRefrigerante = nivelRefrigerante
#         self.nivelLiquidoDireccion = nivelLiquidoDireccion
#         self.soat = soat
#         self.seguroContractual = seguroContractual
#         self.seguroExtraContractual = seguroExtraContractual
#         self.mecanicoAsignado = mecanicoAsignado
#         self.fecha = fecha

#     def __repr__(self):
#         return f"<vehiculos {self.id}>"
    

# class LiquidoRepuesto(Base):
#     __tablename__ = 'liquidosRepuestos'

#     idRegistro = Column('idRegistro', Integer, primary_key=True, autoincrement=True)
#     nivelAceite = Column('nivelAceite', String(15), nullable=False)
#     nivelLiquidoFrenos = Column('nivelLiquidoFrenos', String(15), nullable=False)
#     nivelRefrigerante = Column('nivelRefrigerante', String(15), nullable=False)
#     nivelLiquidoDireccion = Column('nivelLiquidoDireccion', String(15), nullable=False)
#     documentoMecanico = Column('documentoMecanico', String(20), nullable=False)
#     repuestos = Column('repuestos', String(200), nullable=False)
#     placaVehiculo = Column('placa', String(15), ForeignKey('vehiculos.placa', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
#     placa = relationship("Vehiculo", back_populates="liquidosRepuestos")
#     fecha = Column('fecha', DateTime, server_default=func.now(), nullable=True)

#     def __init__(self, idRegistro, nivelAceite, nivelLiquidoFrenos, nivelRefrigerante, nivelLiquidoDireccion, documentoMecanico, repuestos, placaVehiculo, fecha):
#         self.idRegistro = idRegistro
#         self.nivelAceite = nivelAceite
#         self.nivelLiquidoFrenos = nivelLiquidoFrenos
#         self.nivelRefrigerante = nivelRefrigerante
#         self.nivelLiquidoDireccion = nivelLiquidoDireccion
#         self.documentoMecanico = documentoMecanico
#         self.repuestos = repuestos
#         self.placaVehiculo = placaVehiculo
#         self.fecha = fecha

#     def __repr__(self):
#         return f"<liquidosRepuestos {self.id}>"

    