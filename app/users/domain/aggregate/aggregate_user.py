from app.users.domain.entities.user import User  
from app.common.domain.entity import Entity
from app.users.domain.value_object.id import Id

class AggregateUser(Entity):
    def __init__(self,id: Id, user: User):
        self.id = id
        self.user = user

    def get(self):
        return self.user

    @classmethod
    def create(cls, id: str, name: str, username: str, email: str, password: str, role: str):
        user = User.create(id, name, username, email, password, role)
        return cls(id,user)

    def update(self, username: str = None, email: str= None, password: str =None, name: str = None):
        self.user.update(username, email, password, name)