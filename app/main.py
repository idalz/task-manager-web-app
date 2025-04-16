from fastapi import FastAPI
from app.routes import task as routes


app = FastAPI()

app.include_router(routes.router)
