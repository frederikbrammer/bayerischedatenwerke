from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cases, stats

app = FastAPI(
    title="Bayerische Datenwerke API",
    description="API for legal case management",
    version="0.1.0"
)

# Configure CORS to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cases.router, prefix="/api")
app.include_router(stats.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Bayerische Datenwerke API"}