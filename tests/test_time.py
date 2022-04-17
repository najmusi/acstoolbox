# import sys
# sys.path.append('/Volumes/Kingston128/Sandbox/exastris/')
from acstoolbox.foundation import rotation
from acstoolbox.time import time
import numpy as np

def test_julian_date_from_gregorian():
    time_class = time.Time()
    desiredJD = 2451545.0
    assert time_class.UTCtoJDUTC(2000, 1, 1, 12, 0, 0)  == desiredJD
    vX = rotation.vX(np.array([0,1,2]))
    assert  vX[0,0]== 0
