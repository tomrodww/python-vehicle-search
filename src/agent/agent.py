import re
import requests # make requests to the server, connection with the fastAPI, GET method
from src.constants import BRANDS, COLORS, MIN_YEAR, MAX_YEAR, MODELS, ENGINES, TRANSMISSIONS, CATEGORIES, FUEL_TYPES, MIN_PRICE_CENTS, MAX_PRICE_CENTS, MIN_MILEAGE, MAX_MILEAGE

API_URL = "http://127.0.0.1:8000" #Server URL

class VehicleAgent:
    def __init__(self):
        self.filtered_vehicles = []
        self.filters = {}
                
    def get_filters(self, text):
        filters = {}
        
        # filter brand
        for brand in BRANDS:
            if brand.lower() in text.lower():
                filters['brand'] = brand.lower()
                break

        color_variations = {
            'vermelho': r'vermelh[ao]',
            'azul': r'azul',
            'verde': r'verde',
            'cinza': r'cinz[ao]',
            'preto': r'pret[ao]',
            'branco': r'branc[ao]',
            'prata': r'prat[ao]'
        }
        # filter color
        for color in color_variations:
            if color.lower() in text.lower():
                filters['color'] = color.lower()
                break

        # filter year
        year_match = re.search(r'\b(19\d{2}|20\d{2})\b', text)
        if year_match:
            year = int(year_match.group(1))
            if MIN_YEAR <= year <= MAX_YEAR:
                if 'até' in text.lower() or 'antes' in text.lower() or 'máximo' in text.lower():
                    filters['year_max'] = year
                elif 'a partir' in text.lower() or 'após' in text.lower() or 'mínimo' in text.lower():
                    filters['year_min'] = year
                else:
                    filters['year'] = str(year)
        
        # filter model
        for brand, models in MODELS.items():
            for model in models:
                if model.lower() in text.lower():
                    filters['model'] = model.lower()
                    # if no brand yet, automatically set it
                    if 'brand' not in filters:
                        filters['brand'] = brand.lower()
                    break
            if 'model' in filters:
                break
            
        # filter engine
        for engine in ENGINES:
            if engine.lower() in text.lower():
                filters['engine'] = engine.lower()
                break
        
        # filter transmission
        for transmission in TRANSMISSIONS:
            if transmission.lower() in text.lower():
                filters['transmission'] = transmission.lower()
                break

        # filter fuel type
        for fuel_type in FUEL_TYPES:
            if fuel_type.lower() in text.lower():
                filters['fuel_type'] = fuel_type.lower()
                break
        
        # filter category
        for category in CATEGORIES:
            if category.lower() in text.lower():
                filters['category'] = category.lower()
                break
        
        # filter sunroof (only if explicitly mentioned)
        if 'teto solar' in text.lower():
            filters['sunroof'] = True

        # filter mileage
        mileage_match = re.search(r'\b(\d+)\s*(?:mil\s+km|mil\s+quilômetros?|km|quilômetros?)\b', text.lower())
        if mileage_match:
            number = int(mileage_match.group(1))
            unit = mileage_match.group(0).split()[-1]  # get the last word (km or quilômetros)
            
            # if 'mil' multiply by 1000
            if 'mil' in mileage_match.group(0):
                mileage = number * 1000
            else:
                mileage = number
            
            if 'até' in text.lower() or 'antes' in text.lower() or 'máximo' in text.lower():
                filters['mileage_max'] = mileage
            elif 'a partir' in text.lower() or 'após' in text.lower() or 'mínimo' in text.lower():
                filters['mileage_min'] = mileage
            else:
                filters['mileage_max'] = mileage  # makes max as default

        # filter price
        price_match = re.search(r'\b(?:r\$\s*)?(\d+(?:\.\d{3})*(?:,\d{2})?)\s*(?:mil\s+reais?|reais?)\b', text.lower())
        if price_match:
            number_str = price_match.group(1).replace('.', '').replace(',', '.')
            number = float(number_str)
            
            # if 'mil' multiply by 1000, also multiply by 100 to convert to cents
            if 'mil' in price_match.group(0):
                price = int(number * 1000 * 100)
            else:
                price = int(number * 100)
            
            if 'até' in text.lower() or 'antes' in text.lower() or 'máximo' in text.lower():
                filters['price_max'] = price
            elif 'a partir' in text.lower() or 'após' in text.lower() or 'mínimo' in text.lower():
                filters['price_min'] = price
            else:
                filters['price_max'] = price  # makes max as default

        # Check if any new filters were found
        if len(filters) > 0:
            # Add new filters to existing ones
            self.filters.update(filters)
            return True  # Indicates new filters were applied
        else:
            # No new filters found, keep previous filters
            return False  # Indicates no new filters were applied
    
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
            
                # List/show vehicles
                if user_input in ['listar', 'mostrar', 'exibir', 'buscar', 'procurar']:
                    if self.filtered_vehicles:
                        if self.filters:
                            print(f'Listando veículos filtrados por: {self.filters}')
                        else:
                            print('Listando todos os veículos.')
                        self.display_vehicles_table()
                    else:
                        print("Nenhum veículo filtrado. Faça uma busca primeiro.")
                    continue

                # reset filters
                if user_input in ['resetar', 'reset', 'limpar']:
                    self.filters = {}
                    self.filtered_vehicles = []
                    print('Filtros resetados.')
                    continue

                # remove specific filters
                if user_input in ['remover', 'remover filtro', 'remover filtro']:
                    self.get_filters(user_input)
                    continue

                # exit app
                if user_input in ['sair', 'encerrar', 'fechar']:
                    break

                # apply filters
                old_filters = self.filters.copy()
                filters_applied = self.get_filters(user_input)
            
                # If new filters were applied, search and filter again
                if filters_applied:
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
                        if 'year_min' in self.filters and matches:
                            if v['year'] < self.filters['year_min']:
                                matches = False
                        if 'year_max' in self.filters and matches:
                            if v['year'] > self.filters['year_max']:
                                matches = False
                        
                        # check price filter
                        if 'price' in self.filters and matches:
                            if v['price_cents'] < self.filters['price']:
                                matches = False
                        if 'price_min' in self.filters and matches:
                            if v['price_cents'] < self.filters['price_min']:
                                matches = False
                        if 'price_max' in self.filters and matches:
                            if v['price_cents'] > self.filters['price_max']:
                                matches = False
                        
                        # check mileage filter
                        if 'mileage' in self.filters and matches:
                            if v['mileage'] < self.filters['mileage']:
                                matches = False
                        if 'mileage_min' in self.filters and matches:
                            if v['mileage'] < self.filters['mileage_min']:
                                matches = False
                        if 'mileage_max' in self.filters and matches:
                            if v['mileage'] > self.filters['mileage_max']:
                                matches = False
                        
                        if matches:
                            self.filtered_vehicles.append(v)
                
                    print(f'Encontrei {len(self.filtered_vehicles)} veículos:')
                    filter_display = []
                    for key, value in self.filters.items():
                        if key == 'year_min':
                            filter_display.append(f"a partir de {value}")
                        elif key == 'year_max':
                            filter_display.append(f"até {value}")
                        elif key in ['price_min', 'price_max']:
                            # Format price in cents to R$ format
                            price_reais = value / 100
                            formatted_price = f"R$ {price_reais:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                            if key == 'price_min':
                                filter_display.append(f"a partir de {formatted_price}")
                            else:
                                filter_display.append(f"até {formatted_price}")
                        elif key in ['mileage_min', 'mileage_max']:
                            # Format mileage with km
                            if key == 'mileage_min':
                                filter_display.append(f"a partir de {value:,} km".replace(',', '.'))
                            else:
                                filter_display.append(f"até {value:,} km".replace(',', '.'))
                        else:
                            filter_display.append(str(value))
                    print(f'Filtros aplicados: {", ".join(filter_display)}')
                    continue
                else:
                    # if no filters applied, show error 
                    print(f'Filtro "{user_input}" não reconhecido.')
                    print('Filtros disponíveis: marcas (BMW, Honda, etc.), cores (vermelho, azul, etc.), anos (2020-2025)')
                    print(f'Filtros atuais mantidos: {self.filters}')
            except Exception as e:
                print(f'Erro: {e}')
                break
            
        


