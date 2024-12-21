from app.common.domain.value_object import ValueObject

class Email(ValueObject):
    def __init__(self, email: str):
       self.email = email

    @classmethod
    def create(cls, email: str):
        return cls(email)
      
    
    def get(self):
        return self.email

  