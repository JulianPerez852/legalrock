from fastapi import FastAPI
from app.routers import test_router
from app.routers import conversation_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    #"http://localhost",  # Reemplaza con la URL de tu aplicación Angular
    #"http://localhost:4200",  # Puerto por defecto de Angular
    # Añade más orígenes según sea necesario
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(test_router.router, prefix="/example", tags=["example"])
app.include_router(conversation_router.conversation_router, prefix="/conversation", tags=["conversation"])