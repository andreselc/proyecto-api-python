from app.common.domain.value_object import ValueObject

class Password(ValueObject):

    def __init__(self, password: str):
        self.password = password
    
    @classmethod
    def create(cls, password: str):
        return cls(password)
    
    def get(self):
        return self.password
