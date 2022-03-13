import numpy as np
from acs_toolbox.constants.celestial_constants import *
from acs_toolbox.time import time
from acs_toolbox.constants.time_constants import *

def wrap_SI(deg):
    return np.mod(deg, 360.0)/180.0*np.pi

class Sun:
    def __init__(self, time):
        """ Low Precision Sun Vector
        Source: Astronomical Almanac 1992:C24
        Accuracy: 0.01 deg
        
        Inputs: 1. Time object
        Output: 1. Sun vector in MOD frame

        Comments: This is a low precision algorithm with an accuracy of 0.01 degrees
                  in the MOD frame.
        """

        self.time_ = time

    def GetMODFromTUT1(self, t_ut1):
        # Approx.
        t_tdb = t_ut1

        lambda_mean = wrap_SI(280.460 + 36000.771*t_ut1)
        theta_mean = wrap_SI(357.5277233 + 35999.05034*t_tdb)
        lambda_ecliptic = wrap_SI(lambda_mean/np.pi*180.0 + 1.914666471*np.sin(theta_mean) + 0.019994643*np.sin(2*theta_mean))
        obliquity = wrap_SI(23.439291 - 0.0130042*t_tdb)

        r_AU_mag = 1.000140612 - 0.016708617*np.cos(lambda_mean) - 0.000139589*np.cos(2*theta_mean)
        r_s = np.array([np.cos(lambda_ecliptic), np.cos(obliquity)*np.sin(lambda_ecliptic/180*np.pi), np.sin(obliquity)*np.sin(lambda_ecliptic)])

        return r_AU_mag*r_s*kAUm

    def GetMODFromJSJ2000UTC(self, js_j2000_utc):
        jd_utc = self.time_.JSJ2000UTCtoJDUTC(js_j2000_utc)
        mjd_utc = self.time_.MJD(jd_utc)
        dut1_s = self.time_.GetEarthObservationParameter(mjd_utc, 'dUT1_s')
        t_ut1 = self.time_.JDtoT(jd_utc + dut1_s/kDayInSeconds)

        return self.GetMODFromTUT1(t_ut1)

    def GetMODPosition(self, y, m, d, mm, hh, ss):
        """Example Use
            clock = time.Time()
            sun = Sun(clock)
            s_mod = sun.GetMODPosition(2006, 4, 2, 0, 0, 0)
        """

        t_ut1 = self.time_.UTCtoTUT1(y, m, d, hh, mm, ss)

        return self.GetMODFromTUT1(t_ut1)
