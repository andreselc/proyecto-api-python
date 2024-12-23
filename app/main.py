from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.users.infrastructure.controller.userController import router as user_router
from app.users.infrastructure.events.boot_event import boot_superadmin

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)

#endpoint de prueba
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def on_startup():
    await boot_superadmin()
    
        
        

