from fastapi import FastAPI
from routes.auth_route import router as user_router
from db import engine

app = FastAPI()



# inclure les routes
app.include_router(user_router, prefix="/api/auth")