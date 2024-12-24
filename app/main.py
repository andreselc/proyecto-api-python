from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.products.infrastructure.controllers.productController import router as product_router  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router, prefix="/api")

#endpoint de prueba
@app.get("/")
def root():
    return {"message": "Hello World"}



