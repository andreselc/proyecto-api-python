from enum import Enum

class Role(str, Enum):
    superadmin = "superadmin"
    manager = "manager"
    customer = "customer"