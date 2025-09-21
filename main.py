from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes.auth_route import router as auth_router
from routes.course_route import router as course_router
from db import engine, init_db

# Importer tous les modèles pour que SQLModel les reconnaisse
from models.user import User
from models.course import Course

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (si besoin de nettoyage)

app = FastAPI(
    title="E-Learning API",
    description="API pour une plateforme d'apprentissage en ligne",
    version="1.0.0",
    lifespan=lifespan
)

# inclure les routes
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(course_router, prefix="/api/courses", tags=["Courses"])