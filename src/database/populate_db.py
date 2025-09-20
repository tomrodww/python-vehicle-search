from src.models import Vehicles, SessionLocal
from src.constants import BRANDS, MODELS, COLORS, ENGINES, TRANSMISSIONS, CATEGORIES, FUEL_TYPES, MIN_YEAR, MAX_YEAR, MIN_PRICE_CENTS, MAX_PRICE_CENTS, MIN_MILEAGE, MAX_MILEAGE
import random

def bool_to_portuguese(value):
    return "Sim" if value else "Não"

def create_vehicles_db():
    # Create database session
    db = SessionLocal()
    
    try:
        db.query(Vehicles).delete()  # clean database
        
        # Add vehicles in the database
        for i in range(400):
            # Generate random values for each vehicle
            brand = random.choice(BRANDS)
            model = random.choice(MODELS[brand])
            year = random.randint(MIN_YEAR, MAX_YEAR)
            price_cents = random.randint(MIN_PRICE_CENTS, MAX_PRICE_CENTS)
            color = random.choice(COLORS)
            mileage = random.randint(MIN_MILEAGE, MAX_MILEAGE)
            engine = random.choice(ENGINES)
            transmission = random.choice(TRANSMISSIONS)
            category = random.choice(CATEGORIES)
            fuel_type = random.choice(FUEL_TYPES)
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
    create_vehicles_db()  # create the vehicles database
