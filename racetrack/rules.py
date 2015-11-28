"""Define rules of the game.
"""


from racetrack.linalg import *


class AccelerationRule(object):
    """Defines the maximal allowed acceleration.

    This is an abstract class that defines the interface to
    acceleration rules.  Concrete rules are derived from this class
    and must define the class variables Norm and AccelMax.  Note that
    (child classes of) AccelerationRule only defines a class method
    and does not need to get instatiated.
    """

    Norm = None
    AccelMax = None

    @classmethod
    def isAllowed(cls, accel):
        if cls.Norm is None or cls.AccelMax is None:
            raise NotImplemented
        return cls.Norm(accel) <= cls.AccelMax


class EightNeighboursRule(AccelerationRule):
    """Eight neighbours rule: 
    the acceleration is constraint to the eight neighbours of zero.
    """
    Norm = Vector.norminf
    AccelMax = 1

class FourNeighboursRule(AccelerationRule):
    """Four neighbours rule: 
    the acceleration is constraint to the four direct neighbours of zero.
    """
    Norm = Vector.norm1
    AccelMax = 1

class EuclideanTenRule(AccelerationRule):
    """Euclidean 10 rule: 
    the Euclidean norm of the acceleration is bound to less or equel ten.
    """
    Norm = Vector.norm2
    AccelMax = 10
