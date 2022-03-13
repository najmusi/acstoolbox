# Standard libraries.
import numpy as np

'''Mathematical Foundations
This module contains functions used for creating rotations using the SO(3)
3D Rotational Group. These special orthogonal matrices are the foundation 
for all attitude representations.
'''

def is_column(v):
    assert v.shape == (3,), f"Vector {v} is *not* a column of size (3,). \nAssign vectors in the following format 'numpy.array([[1],[2],[3]])'"
    return (1 == 1)

def vX(v):
    # Construct the cross-matrix which enables cross products in R3.
    is_column(v)
    return np.array([[0, -v[2], v[1]],[v[2], 0, -v[0]],[-v[1], v[0], 0]])

def EulerAxis(a, phi):
    # Construct a rotation matrix using the axis (a) and angle (phi) of rotation.
    is_column(a)
    return (np.cos(phi)*np.identity(3)) + (1-np.cos(phi))*np.outer(a,a) - np.sin(phi)*vX(a)