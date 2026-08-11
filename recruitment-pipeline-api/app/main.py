from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from . import models, seed
from .database import engine, SessionLocal
from .routers import candidates

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed.seed_database(db)
    finally:
        db.close()
    yield

app = FastAPI(title="Recruitment Pipeline API", lifespan=lifespan)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(candidates.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Recruitment Pipeline API"}
