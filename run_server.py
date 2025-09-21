# simplifying the server command start, was "python -m src.mcp_server.mcp_server" and now is "python run_server.py"
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.mcp_server.mcp_server import app
import uvicorn

if __name__ == "__main__":
    print("Iniciando Servidor MCP de Busca de Veículos...")
    print("Servidor disponível em: http://127.0.0.1:8000")
    print("Endpoint MCP: http://127.0.0.1:8000/mcp")
    print("Documentação da API: http://127.0.0.1:8000/docs")
    print("Pressione CTRL+C para parar o servidor")
    print("-" * 50)
    
    uvicorn.run("src.mcp_server.mcp_server:app", host="0.0.0.0", port=8000, reload=True)
