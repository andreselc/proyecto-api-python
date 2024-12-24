from app.users.domain.aggregate.aggregate_user import AggregateUser
from app.users.infrastructure.model.ModelUser import User
from app.users.domain.entities.user import User
from app.users.domain.value_object.email import Email
from app.users.domain.value_object.id import Id
from app.users.domain.value_object.name import Name
from app.users.domain.value_object.password import Password
from app.users.domain.value_object.username import Username
from app.users.domain.enums.roleEnum import Role


def model_to_Aggregate(user_model: User) -> AggregateUser:
    
    user= User(
        id= Id(user_model.id),
        name = Name(user_model.name), 
        username = Username(user_model.username), 
        email = Email(user_model.email),
        role = Role(user_model.role),
        password= Password(user_model.password)
    )
    return AggregateUser(id= Id(user_model.id),user= user)
