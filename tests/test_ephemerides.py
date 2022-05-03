from acstoolbox.time.clock import Clock
from acstoolbox.ephemerides.sun import Sun

import numpy as np
import pytest as pytest

# TODO
# 1. Evaluate unit sun vector from JS from J2000 (in TT, not UTC)
# 2. Updated test_sun_vector_from_utc using current Astronomical Almanac

# 1. Evaluate unit sun vector from UTC Gregorian date.
def test_sun_vector_from_utc():
    clock = Clock()
    sun = Sun(clock)

    # Evaluate the sun vector in the MOD frame on 2 April 2006 00hh00mm00ss.
    epoch_gregorian_utc = [2006, 4, 2, 0, 0, 0]
    s_mod = sun.GetUnitMODPositionFromUTC(epoch_gregorian_utc)

    # Astronomical Almanac (ICRS).
    s_mod_almanac = np.array([0.9776782, 0.1911521, 0.0828717])

    # Test the accuracy of each unit vector component.
    assert s_mod == pytest.approx(s_mod_almanac, 1e-2)

    # Test the angular difference of the unit sun vector.
    us_mod_almanac = s_mod_almanac / np.linalg.norm(s_mod_almanac)
    dphi = np.arccos(np.dot(s_mod, us_mod_almanac)) / np.pi * 180.0
    assert dphi < 1e-1
