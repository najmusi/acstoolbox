from acstoolbox.time.time import Clock
from acstoolbox.constants.time_constants import (
    DAY_IN_SECONDS,
    JD_J2000,
    MODIFIED_JULIAN_DATE_OFFSET,
    ATOMIC_TO_TERRESTRIAL_S,
)
import numpy as np
import pytest as pytest

# TODO
# 1. Load clock once in fixture
# 1. Confirm if GetdUT1fromGregorian and UTCGregotianToJDUT1 can be removed.
# 1. Confirm if self methods can be converted to cls methods
# 1. In test_julian_centuries add reference for epoch_centuries_from_j2000
# 1. In test_julian_date test for each before/after epoch when a leap second is added

# Additional tests to add.
# 1. EOP lookup for date that is out of bounds
# 1. EOP download

# UTCtoJDUTC
# Convert Gregorian to Julian Date.
def test_gregorian_to_julian_date():
    # J2000 (January 1, 2000 12hh00mm00ss).
    gregorian_j2000 = [2000, 1, 1, 12, 0, 0]

    # Initialize clock and convert Gregorian date.
    clock = Clock()
    assert clock.GregorianToJulianDate(gregorian_j2000) == JD_J2000


# GregorianToJSJ2000
# Convert Gregorian to Julian seconds from J2000.
def test_gregorian_to_julian_seconds_from_j2000():
    # JS from J2000 for January 1, 2022 00hh00mm00ss UTC.
    JD_EPOCH = 2459580.5
    epoch_js_j2000 = (JD_EPOCH - JD_J2000) * DAY_IN_SECONDS

    # Initialize clock and convert Gregorian date.
    clock = Clock()
    epoch_gregorian = [2022, 1, 1, 0, 0, 0]
    assert clock.GregorianToJSJ2000(epoch_gregorian) == epoch_js_j2000


# JSJ2000ToJD
# Convert Julian seconds from J2000 to Julian Date.
def test_julian_seconds_from_j2000_to_jd():
    # Initialize Clock.
    clock = Clock()

    # January 1, 2022 00hh00mm00ss UTC.
    epoch_gregorian = [2022, 1, 1, 0, 0, 0]
    epoch_js_j2000 = clock.GregorianToJSJ2000(epoch_gregorian)

    # Julian Date from Gregorian date must match JS from J2000 conversion.
    epoch_jd = clock.GregorianToJulianDate(epoch_gregorian)
    assert clock.JSJ2000ToJD(epoch_js_j2000) == epoch_jd


# MJD
# Evaluate Modified Julian Date from Julian Date
def test_modified_julian_date():
    # Initialize clock and evaluate MJD for J2000.
    clock = Clock()
    assert clock.MJD(JD_J2000) == (JD_J2000 - MODIFIED_JULIAN_DATE_OFFSET)


# JDToT
# Evaluate Julian Centuries from J2000
def test_julian_centuries():
    # Initialize clock and set the epoch to April 24, 2022 00hh00mm00ss.
    clock = Clock()
    epoch_gregorian = [2022, 4, 24, 0, 0, 0]
    epoch_centuries_from_j2000 = 0.22309377138945

    # Julian centuries evaluated from JD is equivalent to known quantity.
    epoch_jd = clock.GregorianToJulianDate(epoch_gregorian)
    assert clock.JDToT(epoch_jd) == pytest.approx(epoch_centuries_from_j2000, 1e-6)


# UTCGregorianToUT1JSJ2000
# Evaluate conversion from UTC Gregorian to UT1 JS from J2000.
# This is also a test for MJD lookup since dUT1 must be extrated from the EOP.
def test_gregorianutc_to_jsj2000ut1():
    # Initialize clock and set the epoch to March 24, 2022 12hh00mm00ss.
    clock = Clock()
    epoch_gregorian = [2022, 3, 24, 12, 0, 0]
    epoch_jd = clock.GregorianToJulianDate(epoch_gregorian)
    dUT1_s = (-0.1005632 - 0.1001852) / 2.0  # MJD of 59662.5.

    epoch_js_from_j2000_in_ut1 = (epoch_jd - JD_J2000) * DAY_IN_SECONDS + dUT1_s
    assert clock.UTCGregorianToUT1JSJ2000(epoch_gregorian) == pytest.approx(
        epoch_js_from_j2000_in_ut1, 1e-6
    )


# UTCGregotianToJDUT1
# Evaluate conversion from UTC Gregorian to UT1 JD.
def test_utc_gregorian_to_ut1_jd():
    # Initialize clock and set the epoch to March 24, 2022 12hh00mm00ss.
    clock = Clock()
    epoch_gregorian = [2022, 3, 24, 12, 0, 0]
    dUT1_s = (-0.1005632 - 0.1001852) / 2.0  # MJD of 59662.5.

    clock.UTCGregotianToJDUT1(epoch_gregorian) == (
        clock.GregorianToJulianDate(epoch_gregorian) + dUT1_s / DAY_IN_SECONDS
    )


# UTCGregoriantoTAIJD
# Evaluate conversion from UTC Gregorian to TAI Julian Date.
# This is also a test for a leap second lookup.
def test_utc_to_jd_in_tai():
    # Initialize clock and set the epoch to March 24, 2022 12hh00mm00ss.
    clock = Clock()
    epoch_gregorian = [2022, 3, 24, 12, 0, 0]
    epoch_jd = clock.GregorianToJulianDate(epoch_gregorian)
    dAT_s = -37  # MJD of 59662.5.

    clock.UTCGregoriantoTAIJD(epoch_gregorian) == epoch_jd + dAT_s / DAY_IN_SECONDS


# TAIstoTTs
# Evaluate offset from Atomic to Terrestrial time.
def test_utc_to_jd_in_tai():
    clock = Clock()
    clock.TAIstoTTs(0.0) == ATOMIC_TO_TERRESTRIAL_S


# UTCGregorianToTTSeconds
# Evaluate conversion from UTC Gregorian to Seconds in Terrestrial Time.
def test_utc_to_seconds_in_tt():
    clock = Clock()
    epoch_gregorian_UTC = [2000, 1, 1, 12, 0, 0, 0]
    assert clock.UTCGregorianToTTSeconds(epoch_gregorian_UTC) == (
        (JD_J2000 * DAY_IN_SECONDS + 32) + ATOMIC_TO_TERRESTRIAL_S
    )


# GetdUT1fromGregorian
def test_dut1_from_gregorian():
    # Initialize clock and set the epoch to March 24, 2022 12hh00mm00ss.
    clock = Clock()
    epoch_gregorian = [2022, 3, 24, 12, 0, 0]
    dUT1_s = (-0.1005632 - 0.1001852) / 2.0  # MJD of 59662.5.

    assert clock.GetdUT1fromGregorian(epoch_gregorian) == dUT1_s
