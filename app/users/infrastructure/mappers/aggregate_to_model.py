from app.users.domain.aggregate.aggregate_user import AggregateUser
from app.users.infrastructure.model.ModelUser import User as ModelUser
from datetime import datetime

def Aggregate_to_model(user_aggregate: AggregateUser) -> ModelUser:
    
    return ModelUser(
        id= user_aggregate.user.id.get(),
        name = user_aggregate.user.name.get(),
        username = user_aggregate.user.username.get(), 
        email = user_aggregate.user.email.get(),
        password = user_aggregate.user.password.get(),
        role = user_aggregate.user.role.value,
        created_at =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
