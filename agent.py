import requests # make requests to the server, connection with the fastAPI, GET method

API_URL = "http://127.0.0.1:8000" #Server URL

def bool_to_portuguese(value):
  return "sim" if value else "não"

class VehicleAgent:
  def __init__(self):
    self.filtered_vehicles = []
    self.filters = {}
    
  def get_filters(self, text):
    filters = {}
    
    # filter brand
    brands = ['BMW', 'Honda', 'Tesla', 'Volkswagen', 'Fiat', 'Chevrolet', 'Ford', 'Toyota', 'Hyundai', 'Nissan', 'Renault', 'Peugeot']
    for brand in brands:
      if brand.lower() in text.lower():
        filters['brand'] = brand.lower()
        break

    
    return filters
  
  def search(self):
    response = requests.get(f"{API_URL}/vehicles-list")
    data = response.json()
    return data['vehicles']

  def display_filters(self):
    if self.filters:
      print(f'Filtrando por: {self.filters}')
    else:
      print('Nenhum filtro aplicado.')

  def run(self):
    while True:
      try:
        user_input = input("Você: ").strip().lower()
        filters = self.get_filters(user_input)    
        try:
          vehicles = self.search()
        except Exception as e:
          print(f"Erro ao buscar veículos: {e}")
          continue
        
        if 'brand' in filters and filters['brand']:
          self.filtered_vehicles = []
          for v in vehicles:
            if v['brand'].lower() == filters['brand'].lower():
              self.filtered_vehicles.append(v)
          print(f'Encontrei {len(self.filtered_vehicles)} veículos:')
          print(f'Filtros aplicados: {self.filters}')
          continue

        if user_input in ['listar', 'mostrar', 'exibir']:
          if self.filtered_vehicles:
            for v in self.filtered_vehicles:
              print(f'  {v["brand"]} {v["model"]} - R$ {v["price_cents"]/100:,.0f}')
          else:
            print("Nenhum veículo filtrado. Faça uma busca primeiro.")
          continue

        if user_input in ['sair', 'encerrar', 'fechar']:
          break
        else:
          print(f'Marca "{user_input}" não encontrada.')
          print('Marcas disponíveis: BMW, Honda, Tesla, Volkswagen, Fiat, Chevrolet, Ford, Toyota, Hyundai, Nissan, Renault, Peugeot')
      except Exception as e:
        print(f'Erro: {e}')
        break
    
      


if __name__ == "__main__":
  agent = VehicleAgent() # create an instance of the agent
  agent.run() # run the agent
