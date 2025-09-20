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
                
                vehicles = query.all()
                return MCPResponse(success=True, data=[vehicle.to_dict() for vehicle in vehicles], total=len(vehicles), message=f"Encontrei {len(vehicles)} veículos")
            else:
                return MCPResponse(success=False, message=f"Ação desconhecida: {request.action}")
    
    except Exception as e:
        return MCPResponse(success=False, message=f"Error: {str(e)}")

  
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
