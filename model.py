from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Vehicles(Base):
    __tablename__ = 'vehicles'
    vin = Column(String, primary_key=True)
    manufacturer_name = Column(String)
    description = Column(String)
    horse_power = Column(Integer)
    model_name = Column(String)
    model_year = Column(Integer)
    purchase_price = Column(Float)
    fuel_type = Column(String)