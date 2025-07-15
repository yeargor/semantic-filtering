from enum import Enum

class OperationType(str,Enum):
    CREATE = 'c'
    UPDATE = 'u'
    DELETE = 'd'