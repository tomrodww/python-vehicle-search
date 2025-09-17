from fastapi import FastAPI
from models import Vehicles, SessionLocal

app = FastAPI()

@app.get("/")
def root():
  return {"message": "Hello World"}

@app.get("/vehicles-list")
def vehicles_list():
  db = SessionLocal()
  vehicles = db.query(Vehicles).all()
  return {"vehicles": [vehicle.to_dict() for vehicle in vehicles]}
