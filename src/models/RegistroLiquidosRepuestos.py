import database.db as db
from sqlalchemy import Column, String, DateTime, ForeignKey, func, Integer
from sqlalchemy.orm import relationship

class Vehiculo(db.Base):
    __tablename__ = 'registroLiquidoRepuesto'

    idRegistro = Column('idRegistro', Integer, primary_key=True, autoincrement=True)
    nivelAceite = Column('nivelAceite', String(10), nullable=False)
    nivelLiquidoFrenos = Column('nivelLiquidoFrenos', String(10), nullable=False)
    nivelRefrigerante = Column('nivelRefrigerante', String(10), nullable=False)
    nivelLiquidoDireccion = Column('nivelLiquidoDireccion', String(10), nullable=False)
    documentoMecanico = Column('documentoMecanico', String(20), nullable=False)
    repuestos = Column('repuestos', String(200), nullable=False)
    placaVehiculo = Column('placa', String(15), ForeignKey('vehiculo.placa', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    placa = relationship("Vehiculo", back_populates="registroLiquidoRepuesto")
    fecha = Column('fecha', DateTime, server_default=func.now(), nullable=True)

    def __init__(self, idRegistro, nivelAceite, nivelLiquidoFrenos, nivelRefrigerante, nivelLiquidoDireccion, documentoMecanico, repuestos, placaVehiculo, fecha):
        self.idRegistro = idRegistro
        self.nivelAceite = nivelAceite
        self.nivelLiquidoFrenos = nivelLiquidoFrenos
        self.nivelRefrigerante = nivelRefrigerante
        self.nivelLiquidoDireccion = nivelLiquidoDireccion
        self.documentoMecanico = documentoMecanico
        self.repuestos = repuestos
        self.placaVehiculo = placaVehiculo
        self.fecha = fecha

    def __repr__(self):
        return f"<Earning {self.id}>"