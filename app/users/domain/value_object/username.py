from app.common.domain.value_object import ValueObject

class Username(ValueObject):

    def __init__(self, username: str):
        self.username= username
   
    @classmethod
    def create(cls, username: str):
        return cls(username)

    def get(self):
        return self.username
