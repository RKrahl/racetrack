"""Exception handling.
"""

class RuleViolationError(Exception):
    """A violation of the rules of the games.
    """
    pass


class CollisionError(RuleViolationError):
    """A move of the car caused a collision with a barrier.
    """
    def __init__(self, move, barrier, point):
        self.move = move
        self.barrier = barrier
        self.point = point
        msg = ("Collision of move %s with barrier %s at point %s."
               % (move, barrier, point))
        super(CollisionError, self).__init__(msg)


class AccelerationNotAllowed(RuleViolationError):
    """A not permissible Acceleration.
    """
    def __init__(self, acceleration):
        self.acceleration = acceleration
        msg = ("Acceleration %s is beyond permissible bounds." % 
               (str(acceleration)))
        super(AccelerationNotAllowed, self).__init__(msg)


class NoSolutionError(Exception):
    """No solution found.
    """
    def __init__(self):
        super(NoSolutionError, self).__init__("No solution found.")
