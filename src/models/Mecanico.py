import database.db as db
from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship

class Mecanico(db.Base):
    __tablename__ = 'mecanico'
        
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
        return f"<Account {self.documento}>"