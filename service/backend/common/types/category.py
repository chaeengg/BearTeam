from enum import Enum, unique

@unique
class ObjectCategory(Enum):
    """
    Bicycle
    Kickboard
    Motorcycle
    """
    BICYCLE = 'bicycle'
    KICKBOARD = 'kickboard'
    MOTORCYCLE = 'motorcycle'

    def __int__(self):
        if self == ObjectCategory.BICYCLE:
            return 0
        elif self == ObjectCategory.KICKBOARD:
            return 1
        elif self == ObjectCategory.MOTORCYCLE:
            return 2


@unique
class RiskCategory(Enum):
    """
    Low  = 0
    Mid  = 1
    High = 2
    """
    LOW = 0
    MID = 1
    HIGH = 2

