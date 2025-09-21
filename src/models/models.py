from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Vehicles(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True)
    brand = Column(String)
    model = Column(String)
    year = Column(Integer)
    price_cents = Column(Integer)
    color = Column(String)
    mileage = Column(Integer)
    engine = Column(String)
    transmission = Column(String)
    category = Column(String)
    fuel_type = Column(String)
    sunroof = Column(Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "price_cents": self.price_cents,
            "color": self.color,
            "mileage": self.mileage,
            "engine": self.engine,
            "transmission": self.transmission,
            "category": self.category,
            "fuel_type": self.fuel_type,
            "sunroof": self.sunroof,
        }

engine = create_engine('sqlite:///vehicles.db') # create database
Base.metadata.create_all(engine) # create tables in the database

SessionLocal = sessionmaker(bind=engine) # create a session to interact with the database
