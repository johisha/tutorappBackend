from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import engine, Base
from app.api.v1 import auth, students, teachers, reviews, demo, admin


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TutorConnect API",
    description="Location-based tutor finder platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://127.0.0.1:3000",
        "https://tutorapp-kqyj.onrender.com"
        "https://tutorappbackend.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(reviews.router)
app.include_router(demo.router)
app.include_router(admin.router)



@app.get("/")
def read_root():
    return {"message": "TutorApp API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}