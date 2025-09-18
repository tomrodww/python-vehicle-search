from models import Vehicles, SessionLocal
from faker import Faker
import random

fake = Faker()

def bool_to_portuguese(value):
  return "Sim" if value else "Não"

BRANDS = ['Volkswagen', 'Fiat', 'Chevrolet', 'Ford', 'Honda', 'Toyota', 'Hyundai', 'Nissan', 'Renault', 'Peugeot']
MODELS = {
    'Volkswagen': ['Gol', 'Fox', 'Polo', 'Jetta'],
    'Fiat': ['Uno', 'Palio', 'Strada', 'Argo'],
    'Chevrolet': ['Onix', 'Prisma', 'Celta', 'Corsa'],
    'Ford': ['Ka', 'Fiesta', 'Focus', 'EcoSport'],
    'Honda': ['Civic', 'Fit', 'City', 'HR-V'],
    'Toyota': ['Corolla', 'Etios', 'Yaris', 'Hilux'],
    'Hyundai': ['HB20', 'Creta', 'Tucson', 'Elantra'],
    'Nissan': ['March', 'Versa', 'Kicks', 'Sentra'],
    'Renault': ['Sandero', 'Captur', 'Duster', 'Kwid'],
    'Peugeot': ['208', '308', '2008', '3008']
}

def create_vehicles_db():    
  # Create database session
  db = SessionLocal()
  
  try:
    db.query(Vehicles).delete() #clean database
    
    # Add vehicles in the database
    for i in range(400):
      # Generate random values for each vehicle
      brand = random.choice(BRANDS)
      model = random.choice(MODELS[brand])
      year = random.randint(2010, 2025)
      price_cents = random.randint(1000000, 25000000)
      color = random.choice(['Vermelho', 'Azul', 'Verde', 'Cinza', 'Preto', 'Branco', 'Prata'])
      mileage = random.randint(0, 150000)
      engine = random.choice(['1.0L', '1.3L', '1.5L', '2.0L', '3.0L'])
      transmission = random.choice(['Manual', 'Automático'])
      category = random.choice(['Sedan', 'SUV', 'Hatchback', 'Pickup', 'Van'])
      fuel_type = random.choice(['Gasolina', 'Diesel', 'Elétrico', 'Híbrido'])
      sunroof = random.choice([True, False])
      
      vehicle_data = {
        'brand': brand,
        'model': model,
        'year': year,
        'price_cents': price_cents,
        'color': color,
        'mileage': mileage,
        'engine': engine,
        'transmission': transmission,
        'category': category,
        'fuel_type': fuel_type,
        'sunroof': sunroof
      }
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
      sunroof_text = bool_to_portuguese(vehicle.sunroof)
      print(f"{vehicle.brand} {vehicle.model} {vehicle.year} - R$ {price_reais:,.0f} ({vehicle.color}) - Teto solar: {sunroof_text}")
  finally:
    db.close()

if __name__ == "__main__":
  create_vehicles_db() # create the vehicles database
