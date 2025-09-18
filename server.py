from fastapi import FastAPI
from models import Vehicles, SessionLocal

app = FastAPI()

@app.get("/")
def root():
  return {"message": "Hello World"}

@app.get("/vehicles-list")
def vehicles_list():
  db = SessionLocal() # start database session
  try:
    vehicles = db.query(Vehicles).all()
    return {"vehicles": [vehicle.to_dict() for vehicle in vehicles]}
  finally:
    db.close() # close the session

  
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
