from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import ENGINE, init_db
from app.seed import seed_watchlist

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_watchlist()

    print("Tables Created!")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:5173"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

@app.get("/")
def read_root(): 
    return {"status": "Database Connection Initialized"}