from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Hola, estoy funcionando desde el router"}

@router.get("/hello/{name}")
async def hello_name(name: str):
    return {"message": f"Hola, {name}"}