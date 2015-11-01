"""Define rules of the game.
"""


from racetrack.linalg import *


# Set isAccelerationAllowed to the rule of choice or define your own.

def eight_neighbours_rule(v):
    """Eight neighbours rule: 
    the acceleration is constraint to the eight neighbours of zero.
    """
    return v.norminf() <= 1

def four_neighbours_rule(v):
    """Four neighbours rule: 
    the acceleration is constraint to the four direct neighbours of zero.
    """
    return v.norm1() <= 1

def euclidean_ten_rule(v):
    """Euclidean 10 rule: 
    the Euclidean norm of the acceleration is bound to less or equel ten.
    """
    return v.norm2() <= 10

isAccelerationAllowed = eight_neighbours_rule
