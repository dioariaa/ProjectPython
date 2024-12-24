# models.py
from database.db import Base  # Ensure 'Base' is correctly imported from 'database'
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class MataKuliah(Base):
    __tablename__ = 'matakuliah'
    
    Matkul_ID = Column(Integer, primary_key=True)
    nama_matkul = Column(String)
    sks = Column(Integer)

class Nilai(Base):
    __tablename__ = 'nilai'
    
    Matkul_ID = Column(Integer, ForeignKey('matakuliah.Matkul_ID'), primary_key=True)
    NIM = Column(String, primary_key=True)
    Nilai = Column(Float)
    
    matakuliah = relationship('MataKuliah', backref='nilai')
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}