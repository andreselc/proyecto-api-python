from app.common.domain.value_object import ValueObject

class Id(ValueObject):
    def __init__(self, userid: str):
        self.userid= userid

    @classmethod
    def create(cls, id: str):
        return cls(id)
    
    def get(self) -> str:
        return self.userid  
