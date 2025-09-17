from models import Vehicles, SessionLocal

def create_vehicles_db():    
  sample_vehicles = [
    {
      "brand": "Honda",
      "model": "Civic",
      "year": 2022,
      "price_cents": 12200000,
      "color": "Blue",
      "mileage": 28000,
      "engine": "1.5L Turbo",
      "transmission": "CVT",
      "category": "Sedan",
      "fuel_type": "Flex",
      "sunroof": False
    },
    {
      "brand": "Tesla",
      "model": "Model 3",
      "year": 2023,
      "price_cents": 24000000,
      "color": "White",
      "mileage": 8000,
      "engine": "Electric Motor",
      "transmission": "Single-Speed",
      "category": "Sedan",
      "fuel_type": "Electric",
      "sunroof": True
    },
    {
      "brand": "BMW",
      "model": "X5",
      "year": 2022,
      "price_cents": 15500000,
      "color": "Gray",
      "mileage": 22000,
      "engine": "3.0L I6",
      "transmission": "Automatic",
      "category": "SUV",
      "fuel_type": "Gasoline",
      "sunroof": True
    }
  ]
    
  # Create database session
  db = SessionLocal()
  
  try:
    # Add vehicles in the database
    for vehicle_data in sample_vehicles:
      vehicle = Vehicles(**vehicle_data)
      db.add(vehicle)
  
    # Save the changes in the database
    db.commit()
    
    # Count total vehicles
    total_vehicles = db.query(Vehicles).count()
    print(f"Successfully created {total_vehicles} vehicles in the database!")
    
    # Display vehicles created
    print("\nVehicles added:")
    vehicles = db.query(Vehicles).all()
    for vehicle in vehicles:
      price_reais = vehicle.price_cents / 100
      print(f"{vehicle.brand} {vehicle.model} {vehicle.year} - R$ {price_reais:,.0f} ({vehicle.color})")
  finally:
    db.close()

if __name__ == "__main__":
  create_vehicles_db() # create the vehicles database
