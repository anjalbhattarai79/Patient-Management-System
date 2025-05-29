from fastapi import FastAPI
from app.routes import define_routes

app = FastAPI()  # object of FastAPI
define_routes(app)