from app.users.infrastructure.db.database import get_session
from app.users.application.services.CreateSuperAdmin import CreateSuperAdmin as CreateUserServices
from app.users.infrastructure.repository.UserRepository import UserRepository


async def boot_superadmin():
    async for session in get_session():
        repo = UserRepository(session)
        user_service = CreateUserServices(repo)
        success = await user_service.create_super_admin()
        try:
            success = await user_service.create_super_admin()
            if success:
                print("Superadmin created successfully")
            else:
                print("Superadmin already exists")
        except Exception as e:
            print(f"Error creating superadmin: {e}")