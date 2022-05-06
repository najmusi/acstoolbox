"""ACS Toolbox: SO3 Module
This module contains utility functions for the SO(3) 3D Rotational Group. 
These special orthogonal matrices are the foundation for all attitude representations.
"""

# Standard packages.
import numpy as np

# ACSToolbox packages.
from acstoolbox.foundation.math import is_column, vX


def EulerAxis(a, phi):
    """Construct a rotation matrix using the axis (a) and angle (phi) of rotation."""
    is_column(a)
    return (
        (np.cos(phi) * np.identity(3))
        + (1 - np.cos(phi)) * np.outer(a, a)
        - np.sin(phi) * vX(a)
    )
