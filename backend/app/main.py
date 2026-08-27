from fastapi import FastAPI

app = FastAPI(
    title="ERP Web API",
    description="Backend para el sistema ERP",
    version="0.1.0"
)

@app.get("/")
def home():
    return {"message": "API del ERP funcionando correctamente"}