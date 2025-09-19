import requests # make requests to the server, connection with the fastAPI, GET method

API_URL = "http://127.0.0.1:8000" #Server URL

def bool_to_portuguese(value):
  return "sim" if value else "não"

class VehicleAgent:
  def __init__(self):
    self.filtered_vehicles = []
    self.filters = {}
    
  def get_filters(self, text):
    # filter brand
    brands = ['bmw', 'honda', 'tesla', 'volkswagen', 'fiat', 'chevrolet', 'ford', 'toyota', 'hyundai', 'nissan', 'renault', 'peugeot']
    for brand in brands:
      if brand in text.lower():
        self.filters['brand'] = brand
        break

    # filter color
    colors = ['vermelho', 'azul', 'verde', 'cinza', 'preto', 'branco', 'prata']
    for color in colors:
      if color in text.lower():
        self.filters['color'] = color
        break

    # filter year
    if text.isdigit() and len(text) == 4:
      year = int(text)
      if 2010 <= year <= 2025:
        self.filters['year'] = str(year)
    
    return self.filters
  
  def search(self):
    response = requests.get(f"{API_URL}/vehicles-list")
    data = response.json()
    return data['vehicles']

  def display_vehicles_list(self):
    if self.filters:
      print(f'Listando veículos filtrados por: {self.filters}')
    else:
      print('Listando todos os veículos.')

  def run(self):
    while True:
      try:
        user_input = input("Você: ").strip().lower()
        
        # Handle special commands first
        if user_input in ['listar', 'mostrar', 'exibir']:
          self.display_vehicles_list()
          if self.filtered_vehicles:
            for v in self.filtered_vehicles:
              print(f'  {v["brand"]} {v["model"]} - R$ {v["price_cents"]/100:,.0f}')
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
    
      


if __name__ == "__main__":
  agent = VehicleAgent() # create an instance of the agent
  agent.run() # run the agent
