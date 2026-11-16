from techgear_api.main import app
import uvicorn
import os

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=puerto)
