import database.db as db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

class Vehiculo(db.Base):
    __tablename__ = 'vehiculo'

    placa = Column('placa', String(20), primary_key=True)
    documentoPropietario = Column('documentoPropietario', String(20), nullable=False)
    correoPropietario = Column('correoPropietario', String(60), nullable=False)
    nombrePropietario = Column('nombrePropietario', String(60), nullable=False)
    descripcionVehiculo = Column('descripcionVehiculo', String(200), nullable=False)
    nivelAceite = Column('nivelAceite', String(10), nullable=False)
    nivelLiquidoFrenos = Column('nivelLiquidoFrenos', String(10), nullable=False)
    nivelRefrigerante = Column('nivelRefrigerante', String(10), nullable=False)
    nivelLiquidoDireccion = Column('nivelLiquidoDireccion', String(10), nullable=False)
    soat = Column('soat', String(10), nullable=False)
    seguroContractual = Column('seguroContractual', String(10), nullable=False)
    seguroExtraContractual = Column('seguroExtraContractual', String(10), nullable=False)
    mecanicoAsignado = Column('mecanicoAsignado', String(15), ForeignKey('mecanico.documento', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    mecanico = relationship("Mecanico", back_populates="vehiculo")
    fecha = Column('fecha', DateTime, server_default=func.now(), nullable=True)

    def __init__(self, placa, documentoPropietario, correoPropietario, nombrePropietario, descripcionVehiculo, nivelAceite, nivelLiquidoFrenos, nivelRefrigerante, nivelLiquidoDireccion, soat, seguroContractual, seguroExtraContractual, mecanicoAsignado, fecha):
        self.placa = placa
        self.documentoPropietario = documentoPropietario
        self.correoPropietario = correoPropietario
        self.nombrePropietario = nombrePropietario
        self.descripcionVehiculo = descripcionVehiculo
        self.nivelAceite = nivelAceite
        self.nivelLiquidoFrenos = nivelLiquidoFrenos
        self.nivelRefrigerante = nivelRefrigerante
        self.nivelLiquidoDireccion = nivelLiquidoDireccion
        self.soat = soat
        self.seguroContractual = seguroContractual
        self.seguroExtraContractual = seguroExtraContractual
        self.mecanicoAsignado = mecanicoAsignado
        self.fecha = fecha

    def __repr__(self):
        return f"<Earning {self.id}>"