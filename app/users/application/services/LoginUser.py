from app.users.domain.port.IUserRepository import IUserRepository 
from app.users.application.dtos.LoginUserDto import LoginUserDto
from app.users.application.dtos.LoginRespuestaUserDto import LoginRespuestaUserDto
from app.users.domain.aggregate.aggregate_user import AggregateUser
from app.users.auth.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.users.auth.utils import verify_password
from datetime import timedelta
from fastapi import HTTPException, status

class LoginUser:
    def __init__(self, repo: IUserRepository[AggregateUser]):
        self.repo = repo

    async def loginuser(self, user_dto: LoginUserDto) -> LoginRespuestaUserDto:
        user_aggregate = await self.repo.IsExistUserName(user_dto.username)
        # Verificar si el usuario de ese superadmin
        if user_aggregate is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        hash_password = user_aggregate.user.password.get()
        username = user_aggregate.user.username.get()
        # Verificar si la contraseña es correcta
        if not verify_password(user_dto.password, hash_password ):
           raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password"
            )
        token = create_access_token(data={"sub": username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return LoginRespuestaUserDto(access_token= token, token_type="bearer")
    