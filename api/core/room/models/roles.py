from enum import Enum

class RoleEnum(str, Enum):
    OWNER = "owner"
    MEMBER = "member"