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

        # check if new filters
        if len(filters) > 0:
            # add new filters
            self.filters.update(filters)
            return True
        else:
            return False
    
    def remove_specific_filters(self, text):
        removed_filters = []
        
        # mapping portuguese words to filter
        filter_mappings = {
            'marca': ['brand'],
            'modelo': ['model'],
            'cor': ['color'],
            'ano': ['year', 'year_min', 'year_max'],
            'preço': ['price', 'price_min', 'price_max'],
            'preco': ['price', 'price_min', 'price_max'],
            'quilometragem': ['mileage', 'mileage_min', 'mileage_max'],
            'km': ['mileage', 'mileage_min', 'mileage_max'],
            'motor': ['engine'],
            'transmissão': ['transmission'],
            'combustível': ['fuel_type'],
            'categoria': ['category'],
            'teto solar': ['sunroof']
        }
        
        # remove specific filters
        for term, filter_keys in filter_mappings.items():
            if term in text.lower():
                for key in filter_keys:
                    if key in self.filters:
                        removed_filters.append(self.format_single_filter(key, self.filters[key]))
                        del self.filters[key]
        
        return removed_filters
    
    def format_single_filter(self, key, value):
        if key == 'year_min':
            return f"a partir de {value}"
        elif key == 'year_max':
            return f"até {value}"
        elif key in ['price_min', 'price_max']:
            price_reais = value / 100
            formatted_price = f"R$ {price_reais:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            if key == 'price_min':
                return f"a partir de {formatted_price}"
            else:
                return f"até {formatted_price}"
        elif key in ['mileage_min', 'mileage_max']:
            if key == 'mileage_min':
                return f"a partir de {value:,} km".replace(',', '.')
            else:
                return f"até {value:,} km".replace(',', '.')
        else:
            return str(value)
    
    def format_filters_for_display(self):
        filter_display = []
        for key, value in self.filters.items():
            formatted_value = self.format_single_filter(key, value)
            if key == 'brand':
                filter_display.append(f"Marca: {formatted_value.title()}")
            elif key == 'model':
                filter_display.append(f"Modelo: {formatted_value.title()}")
            elif key == 'color':
                filter_display.append(f"Cor: {formatted_value.title()}")
            elif key == 'year':
                filter_display.append(f"Ano: {formatted_value}")
            elif key == 'year_min':
                filter_display.append(f"Ano mínimo: {formatted_value}")
            elif key == 'year_max':
                filter_display.append(f"Ano máximo: {formatted_value}")
            elif key == 'price_min':
                filter_display.append(f"Preço mínimo: {formatted_value}")
            elif key == 'price_max':
                filter_display.append(f"Preço máximo: {formatted_value}")
            elif key == 'mileage_min':
                filter_display.append(f"Quilometragem mínima: {formatted_value}")
            elif key == 'mileage_max':
                filter_display.append(f"Quilometragem máxima: {formatted_value}")
            elif key == 'engine':
                filter_display.append(f"Motor: {formatted_value.title()}")
            elif key == 'transmission':
                filter_display.append(f"Transmissão: {formatted_value.title()}")
            elif key == 'fuel_type':
                filter_display.append(f"Combustível: {formatted_value.title()}")
            elif key == 'category':
                filter_display.append(f"Categoria: {formatted_value.title()}")
            elif key == 'sunroof':
                filter_display.append(f"Teto solar: {'Sim' if value else 'Não'}")
            else:
                filter_display.append(f"{key.title()}: {formatted_value}")
        return filter_display
    
    def search_and_filter_vehicles(self):
        try:
            mcp_request = {
                "action": "search_vehicles",
                "filters": self.filters
            }
            
            response = requests.post(f"{API_URL}/mcp", json=mcp_request)
            data = response.json()
            
            if data.get("success"):
                self.filtered_vehicles = data.get("data", [])
                return True
            else:
                print(f"Erro: {data.get('message', 'Erro desconhecido')}")
                return False
        except Exception as e:
            print(f"Erro: {e}")
            return False

    def display_vehicles_table(self):
        if not self.filtered_vehicles:
            return
        
        # table header
        print("\n" + "="*160)
        print(f"{'#':<3} {'Marca':<12} {'Modelo':<15} {'Ano':<6} {'Cor':<10} {'Preço':<12} {'Combustível':<12} {'Transmissão':<12} {'Teto solar':<12} {'Categoria':<12} {'Motor':<12} {'Quilometragem':<15}")
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
                    if self.filters:
                        if self.search_and_filter_vehicles():
                            print('Listando veículos filtrados por:')
                            for filter_display in self.format_filters_for_display():
                                print(f'  • {filter_display}')
                            self.display_vehicles_table()
                    else:
                        print("Nenhum filtro aplicado. Faça uma busca primeiro.")
                    continue

                # reset filters
                if user_input in ['resetar', 'reset', 'limpar']:
                    self.filters = {}
                    self.filtered_vehicles = []
                    print('Filtros resetados.')
                    continue

                # remove specific filters
                if any(word in user_input for word in ['limpar', 'remover', 'tirar']):
                    removed_filters = self.remove_specific_filters(user_input)
                    if removed_filters:
                        print('Filtros removidos:')
                        for removed_filter in removed_filters:
                            print(f'  • {removed_filter}')
                        print('Filtros restantes:')
                        for filter_display in self.format_filters_for_display():
                            print(f'  • {filter_display}')
                        # search and filter again with updated filters
                        if self.filters and self.search_and_filter_vehicles():
                            print(f'Encontrei {len(self.filtered_vehicles)} veículos:')
                    else:
                        print('Nenhum filtro específico encontrado para remover.')
                    continue

                # exit app
                if user_input in ['sair', 'encerrar', 'fechar']:
                    break

                # apply filters
                filters_applied = self.get_filters(user_input)
            
                # if new filters, search and show count
                if filters_applied:
                    if self.search_and_filter_vehicles():
                        print(f'Encontrei {len(self.filtered_vehicles)} veículos:')
                        print('Filtros aplicados:')
                        for filter_display in self.format_filters_for_display():
                            print(f'  • {filter_display}')
                    continue
                else:
                    # if no filters applied, show error 
                    print(f'Filtro "{user_input}" não reconhecido.')
                    print('Filtros disponíveis: marcas (BMW, Honda, etc.), cores (vermelho, azul, etc.), anos (2020-2025)')
                    print('Filtros atuais mantidos:')
                    for filter_display in self.format_filters_for_display():
                        print(f'  • {filter_display}')
            except Exception as e:
                print(f"Erro: {e}")
                break
            
        


