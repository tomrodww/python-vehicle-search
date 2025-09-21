import pytest
import sys
import os

# Add the src directory to the path so we can import the agent
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent.agent import VehicleAgent

class TestSingleWords:
    
    def setup_method(self):
        self.agent = VehicleAgent()
    
    def test_single_brand(self):
        self.agent.get_filters("Honda")
        assert self.agent.filters['brand'] == 'honda'
        
        self.agent.filters = {}
        self.agent.get_filters("BMW")
        assert self.agent.filters['brand'] == 'bmw'
    
    def test_single_color(self):
        self.agent.get_filters("branco")
        assert self.agent.filters['color'] == 'branco'
        
        self.agent.filters = {}
        self.agent.get_filters("azul")
        assert self.agent.filters['color'] == 'azul'
    
    def test_single_model(self):
        self.agent.get_filters("civic")
        assert self.agent.filters['model'] == 'civic'
        assert self.agent.filters['brand'] == 'honda'
        
        self.agent.filters = {}
        self.agent.get_filters("gol")
        assert self.agent.filters['model'] == 'gol'
        assert self.agent.filters['brand'] == 'volkswagen'

class TestNaturalLanguage:
    
    def setup_method(self):
        self.agent = VehicleAgent()
    
    def test_brand_and_color(self):
        self.agent.get_filters("quero um honda branco")
        assert self.agent.filters['brand'] == 'honda'
        assert self.agent.filters['color'] == 'branco'
    
    def test_brand_model_color(self):
        self.agent.get_filters("estou procurando um civic azul")
        assert self.agent.filters['brand'] == 'honda'
        assert self.agent.filters['model'] == 'civic'
        assert self.agent.filters['color'] == 'azul'
    
    def test_year_and_price(self):
        self.agent.get_filters("carro de 2020 até 150mil reais")
        assert self.agent.filters['year'] == '2020'
        assert self.agent.filters['price_max'] == 15000000
        print(self.agent.filters)
    
    def test_mileage_and_transmission(self):
        self.agent.get_filters("até 50mil km automático")
        assert self.agent.filters['mileage_max'] == 50000
        assert self.agent.filters['transmission'] == 'automático'
    
    def test_fuel_and_category(self):
        self.agent.get_filters("carro elétrico SUV")
        assert self.agent.filters['fuel_type'] == 'elétrico'
        assert self.agent.filters['category'] == 'suv'
    
    def test_engine_and_sunroof(self):
        self.agent.get_filters("motor 2.0 com teto solar")
        assert self.agent.filters['engine'] == '2.0'
        assert self.agent.filters['sunroof'] == True

class TestComplexNaturalLanguage:
    
    def setup_method(self):
        self.agent = VehicleAgent()
    
    def test_complete_search_phrase(self):
        self.agent.get_filters("estou buscando um honda civic 2020 vermelho até 100mil km automático")
        assert self.agent.filters['brand'] == 'honda'
        assert self.agent.filters['model'] == 'civic'
        assert self.agent.filters['year'] == '2020'
        assert self.agent.filters['color'] == 'vermelho'
        assert self.agent.filters['mileage_max'] == 100000
        assert self.agent.filters['transmission'] == 'automático'
    
    def test_price_range_search(self):
        self.agent.get_filters("quero um BMW até 200mil reais a partir de 2018")
        assert self.agent.filters['brand'] == 'bmw'
        assert self.agent.filters['price_max'] == 20000000  # 200k * 1000 * 100
        assert self.agent.filters['year_min'] == 2018
    
    def test_mileage_range_search(self):
        self.agent.get_filters("carro até 80mil km a partir de 30mil km elétrico")
        assert self.agent.filters['mileage_max'] == 80000
        assert self.agent.filters['mileage_min'] == 30000
        assert self.agent.filters['fuel_type'] == 'elétrico'
    
    def test_year_range_search(self):
        self.agent.get_filters("veículo até 2022 a partir de 2019 SUV")
        assert self.agent.filters['year_max'] == 2022
        assert self.agent.filters['year_min'] == 2019
        assert self.agent.filters['category'] == 'suv'

class TestFilterRemoval:
    
    def setup_method(self):
        self.agent = VehicleAgent()
    
    def test_remove_brand_filter(self):
        self.agent.filters = {'brand': 'honda', 'color': 'vermelho'}
        removed = self.agent.remove_specific_filters("limpar marca")
        assert 'brand' not in self.agent.filters
        assert 'color' in self.agent.filters
        assert len(removed) == 1
    
    def test_remove_multiple_filters(self):
        self.agent.filters = {
            'year': '2020',
            'year_min': 2018,
            'year_max': 2022,
            'brand': 'honda'
        }
        removed = self.agent.remove_specific_filters("limpar filtro de ano")
        assert 'year' not in self.agent.filters
        assert 'year_min' not in self.agent.filters
        assert 'year_max' not in self.agent.filters
        assert 'brand' in self.agent.filters
        assert len(removed) == 3

class TestEdgeCases:
    
    def setup_method(self):
        self.agent = VehicleAgent()
    
    def test_unrecognized_input(self):
        result = self.agent.get_filters("xpto random text")
        assert result == False
        assert len(self.agent.filters) == 0
    
    def test_empty_input(self):
        result = self.agent.get_filters("")
        assert result == False
        assert len(self.agent.filters) == 0
    
    def test_sunroof_only_when_mentioned(self):
        self.agent.get_filters("honda")
        assert 'sunroof' not in self.agent.filters
        
        self.agent.filters = {}
        self.agent.get_filters("honda com teto solar")
        assert self.agent.filters['sunroof'] == True
    
    def test_filter_accumulation(self):
        self.agent.get_filters("honda")
        assert len(self.agent.filters) == 1
        
        self.agent.get_filters("vermelho")
        assert len(self.agent.filters) == 2
        assert self.agent.filters['brand'] == 'honda'
        assert self.agent.filters['color'] == 'vermelho'
