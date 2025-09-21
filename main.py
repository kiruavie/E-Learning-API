from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
async def home():
  return {"home": "E-learning platform"}

