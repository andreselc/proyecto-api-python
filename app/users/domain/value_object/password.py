from app.common.domain.value_object import ValueObject
from app.users.auth.utils import get_password_hash

class Password(ValueObject):

    def __init__(self, password: str):
        self.password = password
    
    @classmethod
    def create(cls, password: str):
        return cls(get_password_hash(password))
    
    def get(self):
        return self.password
