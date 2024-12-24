from app.common.domain.value_object import ValueObject

class Name(ValueObject):
    def __init__(self, nameuser: str):
        self.nameuser = nameuser
    
    @classmethod
    def create(cls, nameuser: str):
        return cls(nameuser)
        
    
    def get(self):
        return self.nameuser