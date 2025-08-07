import uvicorn
from app.main import app

if __name__ == "__main__":
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="error",
        proxy_headers=True
    )
    server = uvicorn.Server(config)
    server.run()