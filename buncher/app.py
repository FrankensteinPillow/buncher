from fastapi import FastAPI
import uvicorn
from config import get_config
from routes import router
from sql import database

CONFIG = get_config()

app: FastAPI = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run(app="app:app", port=CONFIG.service_port)
