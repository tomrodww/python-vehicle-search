from fastapi import FastAPI
from src.models import Vehicles
from src.database.utils import get_db_session
from pydantic import BaseModel
from typing import Dict, Any, List

app = FastAPI(title="Busca de veículos MCP")

class MCPRequest(BaseModel):
    action: str
    filters: Dict[str, Any] = {}

class MCPResponse(BaseModel):
    success: bool
    data: List[Dict] = []
    total: int = 0
    message: str = ""

# MCP - this is creating the endpoint for the MCP
@app.post("/mcp", response_model=MCPResponse)
def mcp_endpoint(request: MCPRequest):
    try:
        with get_db_session() as db:
            if request.action == "search_vehicles":
                query = db.query(Vehicles)
                if request.filters.get("brand"):
                    query = query.filter(Vehicles.brand.ilike(f"%{request.filters['brand']}%"))
                if request.filters.get("year"):
                    query = query.filter(Vehicles.year == request.filters["year"])
                if request.filters.get("color"):
                    query = query.filter(Vehicles.color.ilike(f"%{request.filters['color']}%"))
                if request.filters.get("model"):
                    query = query.filter(Vehicles.model.ilike(f"%{request.filters['model']}%"))
                if request.filters.get("engine"):
                    query = query.filter(Vehicles.engine.ilike(f"%{request.filters['engine']}%"))
                if request.filters.get("transmission"):
                    query = query.filter(Vehicles.transmission.ilike(f"%{request.filters['transmission']}%"))
                if request.filters.get("category"):
                    query = query.filter(Vehicles.category.ilike(f"%{request.filters['category']}%"))
                if request.filters.get("fuel_type"):
                    query = query.filter(Vehicles.fuel_type.ilike(f"%{request.filters['fuel_type']}%"))
                if request.filters.get("sunroof"):
                    query = query.filter(Vehicles.sunroof == request.filters["sunroof"])
                if request.filters.get("price"):
                    query = query.filter(Vehicles.price_cents >= request.filters["price"])
                if request.filters.get("mileage"):
                    query = query.filter(Vehicles.mileage >= request.filters["mileage"])
                
                vehicles = query.all()
                return MCPResponse(success=True, data=[vehicle.to_dict() for vehicle in vehicles], total=len(vehicles), message=f"Encontrei {len(vehicles)} veículos")
            else:
                return MCPResponse(success=False, message=f"Ação desconhecida: {request.action}")
    
    except Exception as e:
        return MCPResponse(success=False, message=f"Error: {str(e)}")

  
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
