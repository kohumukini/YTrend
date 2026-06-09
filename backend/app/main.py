import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import pipeline, silver, watchlist
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

origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

app.include_router(pipeline.router)
app.include_router(silver.router)
app.include_router(watchlist.router)

@app.get("/")
def read_root(): 
    return {"status": "Database Connection Initialized"}