from app.users.domain.entities.user import User  
from app.common.domain.entity import Entity

class AggregateUser(Entity):
    def __init__(self, user: User):
        self.user = user

    def get(self):
        return self.user

    @classmethod
    def create(cls, name: str, username: str, email: str, password: str, role: str):
        user = User.create(name, username, email, password, role)
        return cls(user)

    def update(self, username: str = None, email: str= None, password: str =None):
        self.user.update(username, email, password)