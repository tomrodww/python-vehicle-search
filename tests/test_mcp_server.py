import pytest
from fastapi.testclient import TestClient
from src.mcp_server.mcp_server import app

class TestMCPServer:
    
    def setup_method(self):
        self.client = TestClient(app)

    def test_mcp_endpoint_accessible(self): # tests if the MCP endpoint is accessible and returns correct json structure
        response = self.client.post("/mcp", json={"action": "search_vehicles", "filters": {}})
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify MCP response structure
        assert "success" in data
        assert "data" in data
        assert "total" in data
        assert "message" in data
        
        assert isinstance(data["success"], bool)
        assert isinstance(data["data"], list)
        assert isinstance(data["total"], int)
        assert isinstance(data["message"], str)

        #   this is a sample of the expected response
        #   expected_response_sample = {
        #       "success": true,
        #       "data": [
        #           {
        #           "id": 1,
        #           "brand": "Honda",
        #           "model": "Civic",
        #           "year": 2020,
        #           "price_cents": 8000000,
        #           "color": "Branco",
        #           "mileage": 50000,
        #           "engine": "1.5L",
        #           "transmission": "Automático",
        #           "category": "Sedan",
        #           "fuel_type": "Gasolina",
        #           "sunroof": false
        #           },
        #           {... more vehicles ...}
        #       ],
        #       "total": 400,
        #       "message": "Encontrei 400 veículos"
        #   }
    
    def test_search_vehicles_action_structure(self):
        request_data = {
            "action": "search_vehicles",
            "filters": {"brand": "honda"}
        }
        
        response = self.client.post("/mcp", json=request_data)
        data = response.json()
        
        assert response.status_code == 200
        assert data["success"] == True
        assert "data" in data
        assert "total" in data
        assert "message" in data

        # same response structure but only honda vehicles
    
    def test_invalid_action_handling(self):
        request_data = {
            "action": "invalid_action",
            "filters": {}
        }
        
        response = self.client.post("/mcp", json=request_data)
        data = response.json()
        
        assert response.status_code == 200
        assert data["success"] == False
        assert "Ação desconhecida" in data["message"]

        # returns error message when invalid action is provided to the MCP endpoint