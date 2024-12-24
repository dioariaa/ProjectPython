from fastapi import FastAPI
from controllers.nilai_controller import router as nilai_router  # Correctly import router
from database.db import init_db
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def on_startup():
    init_db()

# Include router
app.include_router(nilai_router, tags=["Nilai"])

# Root endpoint
@app.get("/")
async def root():
    return 
