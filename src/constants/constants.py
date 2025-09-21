# Vehicle brands (standardized to title case)
BRANDS = [
    'BMW', 'Honda', 'Tesla', 'Volkswagen', 'Fiat', 'Chevrolet', 
    'Ford', 'Toyota', 'Hyundai', 'Nissan', 'Renault', 'Peugeot'
]

# Vehicle colors (standardized to title case)
COLORS = [
    'Vermelho', 'Azul', 'Verde', 'Cinza', 'Preto', 'Branco', 'Prata'
]

# Vehicle models by brand
MODELS = {
    'BMW': ['X1', 'X3', 'X5', '320i', '520i'],
    'Honda': ['Civic', 'Fit', 'City', 'HR-V', 'CR-V'],
    'Tesla': ['Model 3', 'Model S', 'Model X', 'Model Y'],
    'Volkswagen': ['Gol', 'Fox', 'Polo', 'Jetta', 'Tiguan'],
    'Fiat': ['Uno', 'Palio', 'Strada', 'Argo', 'Toro'],
    'Chevrolet': ['Onix', 'Prisma', 'Celta', 'Corsa', 'Tracker'],
    'Ford': ['Ka', 'Fiesta', 'Focus', 'EcoSport', 'Ranger'],
    'Toyota': ['Corolla', 'Etios', 'Yaris', 'Hilux', 'RAV4'],
    'Hyundai': ['HB20', 'Creta', 'Tucson', 'Elantra', 'i30'],
    'Nissan': ['March', 'Versa', 'Kicks', 'Sentra', 'Frontier'],
    'Renault': ['Sandero', 'Captur', 'Duster', 'Kwid', 'Logan'],
    'Peugeot': ['208', '308', '2008', '3008', 'Partner']
}

# Engine options
ENGINES = ['1.0L', '1.3L', '1.5L', '2.0L', '3.0L']

# Transmission options
TRANSMISSIONS = ['Manual', 'Automático']

# Vehicle categories
CATEGORIES = ['Sedan', 'SUV', 'Hatchback', 'Pickup', 'Van']

# Fuel types
FUEL_TYPES = ['Gasolina', 'Diesel', 'Elétrico', 'Híbrido']

# Year range
MIN_YEAR = 2010
MAX_YEAR = 2025

# Price range (in cents)
MIN_PRICE_CENTS = 1000000  # R$ 10,000
MAX_PRICE_CENTS = 25000000  # R$ 250,000

# Mileage range
MIN_MILEAGE = 0
MAX_MILEAGE = 150000
