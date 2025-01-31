from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.products.infrastructure.controllers.productController import router as product_router  
from app.users.infrastructure.controller.userController import router as user_router
#importar inventario
from app.inventory.infrastructure.controllers.inventoryController import router as inventory_router
from app.shopping_cart.infrastructure.controllers.shoppinCartController import router as shopping_cart_router
from app.orders.infrastructure.controller.orderController import router as orders_router
from app.reports.infrastructure.controller.reportsController import router as reports_router
#importar carrito
#modulo ordenes
#modulo reporte
from app.users.infrastructure.events.boot_event import boot_superadmin

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(product_router, prefix="/api")
app.include_router(inventory_router)
app.include_router(shopping_cart_router)
app.include_router(orders_router)
app.include_router(reports_router)
#modulo inventario
#modulo carrito
#modulo ordenes
#modulo reporte

#endpoint de prueba
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def on_startup():
    await boot_superadmin()
    
        
        

