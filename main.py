from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import get_db_connection, init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/symbols/{symbol}/annual/{year}")

def get_annual_data(symbol: str, year: str):
    conn = get_db_connection()
