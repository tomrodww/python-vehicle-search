# simplifying the server command start, was "python -m src.mcp_server.mcp_server" and now is "python run_server.py"
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.mcp_server.mcp_server import app
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Vehicle Search MCP Server...")
    print("📍 Server will be available at: http://127.0.0.1:8000")
    print("🔗 MCP endpoint: http://127.0.0.1:8000/mcp")
    print("📚 API docs: http://127.0.0.1:8000/docs")
    print("⏹️  Press CTRL+C to stop the server")
    print("-" * 50)
    
    uvicorn.run("src.mcp_server.mcp_server:app", host="0.0.0.0", port=8000, reload=True)
