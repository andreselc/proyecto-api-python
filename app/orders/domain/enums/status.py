from enum import Enum

class Status(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"