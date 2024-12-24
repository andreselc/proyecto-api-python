from uuid import uuid4
from app.common.domain.value_object import ValueObject

class Id(ValueObject):
    def __init__(self, userid: str):
        self.userid= userid

    @classmethod
    def create(cls):
        return cls(str(uuid4()))
    
    def get(self) -> str:
        return self.userid  