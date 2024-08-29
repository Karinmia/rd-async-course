import enum


class CveState(enum.Enum):
    PUBLISHED = "PUBLISHED"
    RESERVED = "RESERVED"
    REJECTED = "REJECTED"
