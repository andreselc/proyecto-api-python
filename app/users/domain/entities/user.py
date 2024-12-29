from app.users.domain.value_object.email import Email
from app.users.domain.value_object.id import Id
from app.users.domain.value_object.name import Name
from app.users.domain.value_object.password import Password
from app.users.domain.value_object.username import Username
from app.users.domain.enums.roleEnum import Role
from app.common.domain.entity import Entity

class User(Entity):
    def __init__(self, id: Id, name: Name, username: Username, email: Email, password: Password, role: Role):
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.role = role

  
    def get(self):
        return self

    @classmethod
    def create(cls, id:str, name: str, username: str, email: str, password: str, role: str):
        id = Id.create(id)
        name = Name.create(name)
        username = Username.create(username)
        email = Email.create(email)
        password = Password.create(password)
        role= Role(role.lower())
        return cls(id, name, username, email, password, role)

    def update(self, username: str = None, email: str= None, password: str =None, name: str = None):    
        if username:
            self.username = Username.create(username)
        if email:
            self.email = Email.create(email)
        if password:
            self.password = Password.create(password)
        if name:
             self.name = Name.create(name)