import requests # make requests to the server, connection with the fastAPI, GET method

API_URL = "http://127.0.0.1:8000" #Server URL

class VehicleAgent:
  def filter_vehicles(self, text):
    filters = {}
    
    # filter brand
    brands = ['bmw', 'honda', 'tesla']
    for brand in brands:
      if brand in text.lower():
        filters['brand'] = brand
        break
      else:
        filters['brand'] = None 
        break
    return filters
  
  def search(self):
    response = requests.get(f"{API_URL}/vehicles-list")
    return response.json()['vehicles']

  def run(self):
    user_input = input("Type brand name: ")
    filters = self.filter_vehicles(user_input)    
    vehicles = self.search()
    
    # filter vehicles by brand
    if 'brand' in filters:
      vehicles = [v for v in vehicles if v['brand'].lower() == filters['brand']]
    
    print(f'Found {len(vehicles)} vehicles:')
    for v in vehicles:
      print(f'  {v["brand"]} {v["model"]} - R$ {v["price_cents"]/100:,.0f}')

if __name__ == "__main__":
  agent = VehicleAgent() # create an instance of the agent
  agent.run() # run the agent
