import requests # make requests to the server, connection with the fastAPI, GET method
from src.constants import BRANDS, COLORS, MIN_YEAR, MAX_YEAR, MODELS, ENGINES, TRANSMISSIONS, CATEGORIES, FUEL_TYPES, MIN_PRICE, MAX_PRICE, MIN_MILEAGE, MAX_MILEAGE

API_URL = "http://127.0.0.1:8000" #Server URL

class VehicleAgent:
  def __init__(self):
    self.filtered_vehicles = []
    self.filters = {}
    
  def get_filters(self, text):
    # filter brand
    for brand in BRANDS:
      if brand.lower() in text.lower():
        self.filters['brand'] = brand.lower()
        break

    # filter color
    for color in COLORS:
      if color.lower() in text.lower():
        self.filters['color'] = color.lower()
        break

    # filter year
    if text.isdigit() and len(text) == 4:
      year = int(text)
      if MIN_YEAR <= year <= MAX_YEAR:
        self.filters['year'] = str(year)
    
    # filter model
    for model in MODELS:
      if model.lower() in text.lower():
        self.filters['model'] = model.lower()
        break
    
    # filter engine
    for engine in ENGINES:
      if engine.lower() in text.lower():
        self.filters['engine'] = engine.lower()
        break
    
    # filter transmission
    for transmission in TRANSMISSIONS:
      if transmission.lower() in text.lower():
        self.filters['transmission'] = transmission.lower()
        break

    # filter fuel type
    for fuel_type in FUEL_TYPES:
      if fuel_type.lower() in text.lower():
        self.filters['fuel_type'] = fuel_type.lower()
        break
    
    # filter category
    for category in CATEGORIES:
      if category.lower() in text.lower():
        self.filters['category'] = category.lower()
        break
    
    # filter sunroof
    if 'teto solar' in text.lower():
      self.filters['sunroof'] = True
    else:
      self.filters['sunroof'] = False

    return self.filters
  
  def search(self):
    mcp_request = {
      "action": "search_vehicles",
      "filters": self.filters
    }
    
    response = requests.post(f"{API_URL}/mcp", json=mcp_request)
    data = response.json()
    
    if data.get("success"):
      return data.get("data", [])
    else:
      print(f"MCP Error: {data.get('message', 'Unknown error')}")
      return []

  def display_vehicles_table(self):
    if not self.filtered_vehicles:
      return
    
    # table header
    print("\n" + "="*160)
    print(f"{'#':<3} {'Marca':<12} {'Modelo':<15} {'Ano':<6} {'Cor':<10} {'Preço':<12} {'Combustível':<12} {'Transmissão':<12} {'Teto solar':<12} {'Categoria':<12} {'Motor':<12} {'Quilometragem':<15} ")
    print("="*160)
    
    # table rows
    for i, v in enumerate(self.filtered_vehicles, 1):
      price = f"R$ {v['price_cents']/100:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')
      sunroof = "Sim" if v['sunroof'] else "Não"
      mileage = f"{v['mileage']:,}".replace(',', '.')

      
      print(f"{i:<3} {v['brand']:<12} {v['model']:<15} {v['year']:<6} {v['color']:<10} {price:<12} {v['fuel_type']:<12} {v['transmission']:<12} {sunroof:<12} {v['category']:<12} {v['engine']:<12} {mileage:<15}")
    
    print("="*160)
    print(f"Total: {len(self.filtered_vehicles)} veículos encontrados\n")

  def run(self):
    while True:
      try:
        user_input = input("Você: ").strip().lower()
        
        # Handle special commands first
        if user_input in ['listar', 'mostrar', 'exibir']:
          if self.filtered_vehicles:
            if self.filters:
              print(f'Listando veículos filtrados por: {self.filters}')
            else:
              print('Listando todos os veículos.')
            self.display_vehicles_table()
          else:
            print("Nenhum veículo filtrado. Faça uma busca primeiro.")
          continue

        if user_input in ['sair', 'encerrar', 'fechar']:
          break

        # apply filters
        old_filters = self.filters.copy()
        self.get_filters(user_input)
        
        # If new filters, search and filter again
        if self.filters != old_filters:
          try:
            vehicles = self.search()
          except Exception as e:
            print(f"Erro ao buscar veículos: {e}")
            continue
          
          self.filtered_vehicles = []
          for v in vehicles:
            matches = True
            
            # check brand filter
            if 'brand' in self.filters:
              if v['brand'].lower() != self.filters['brand'].lower():
                matches = False
            
            # check color filter
            if 'color' in self.filters and matches:
              if v['color'].lower() != self.filters['color'].lower():
                matches = False
            
            # check year filter
            if 'year' in self.filters and matches:
              if str(v['year']) != self.filters['year']:
                matches = False
            
            if matches:
              self.filtered_vehicles.append(v)
          
          print(f'Encontrei {len(self.filtered_vehicles)} veículos:')
          print(f'Filtros aplicados: {self.filters}')
          continue

        # if no filters applied, show error 
        print(f'Filtro "{user_input}" não reconhecido.')
        print('Filtros disponíveis: marcas (BMW, Honda, etc.), cores (vermelho, azul, etc.), anos (2020-2025)')
      except Exception as e:
        print(f'Erro: {e}')
        break
    
      


