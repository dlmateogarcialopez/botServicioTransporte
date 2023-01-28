import database.db as db
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

class Liquido_Repuesto(db.Base):

    __tablename__ = 'Liquidos_Repuestos'
    
    idRegistro = Column('idRegistro', String(15), primary_key=True, nullable=False)
    nivelAceite = Column('nivelAceite', String(15),  nullable=False)
    nivelLiquidoFrenos = Column('nivelLiquidoFrenos', String(15), nullable=False)
    nivelRefrigerante = Column('nivelRefrigerante', String(15), nullable=False)
    nivelLiquidoDireccion = Column('nivelLiquidoDireccion', String(15),  nullable=False)
    documentoMecanico = Column('documentoMecanico', String(15), nullable=False)
    repuestos = Column('repuestos', String(15), nullable=False)
    placa = Column('placa', String(15), nullable=False)
    #vehiculos = relationship('Vehiculo', back_populates='Liquidos_Repuestos')
    
    def __init__(self, idRegistro, nivelAceite, nivelLiquidoFrenos, nivelRefrigerante, nivelLiquidoDireccion, documentoMecanico, repuestos, placa ):
        self.idRegistro = idRegistro
        self.nivelAceite = nivelAceite
        self.nivelLiquidoFrenos = nivelLiquidoFrenos
        self.nivelRefrigerante = nivelRefrigerante
        self.nivelLiquidoDireccion = nivelLiquidoDireccion
        self.documentoMecanico = documentoMecanico
        self.repuestos = repuestos
        self.placa = placa
    
    def __repr__(self):
        return f"<Liquido_Repuesto {self.idRegistro}>"
