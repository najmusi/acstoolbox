from acstoolbox.constants.time_constants import *
import math
import numpy as np
import os
import pandas as pd

def ConstructEarthObservationParameterTables():
    # TODO: Convirm infer_nrows to determine negative values of columns
    eop_file = os.getcwd() + "/EOP.txt"
    header_list = ['year', 'month', 'date', 'mjd', 'x_arcsec', 'y_arcsec',
                   'dUT1_s', 'LOD_s', 'dX_arcsec', 'dY_arcsec', 'x_Err_arcsec',
                   'y_err_arcsec', 'dUT1_err_s', 'LOD_err_s', 'dX_err_arcsec',
                   'dY_err_arcsec']
    df = pd.read_fwf(eop_file, sep=" ",
                     names=header_list,
                     infer_nrows=1000)

    return df

def IsLeapYear(yyyy):
    # TODO: When the year is a century-multiple, 
    # it is only a leap year if divisible by 400.
    if (yyyy % 4 == 0):
        return (1==1)
    
    return (0==1)

def GetDaysInEachMonth():
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    return days_in_month

def DayofYear(yyyy, mm, dd, h, m, s):
    # Day of the year is not the same as days elapsed.
    # Ex. the day of the year on Jan 1 at noon is 1.5, 
    # even though a full day has not passed
    days_in_month = GetDaysInEachMonth()
    
    if IsLeapYear(yyyy):
        days_in_month[1] += 1

    # Numebr of days up to the month.
    # TODO: Use constants.
    days = sum(days_in_month[0:mm]) + dd + h/24 + m/1440 + s/86400

    return days

def YearFractionalDaystoJDUTC(yyyy, total_fractional_days):
    days_per_month = GetDaysInEachMonth()
    if IsLeapYear(yyyy):
        days_per_month[1] = 29
    
    mm = 0
    full_months_in_days = 0
    for month in np.linspace(0,11,12):
        days_up_to_month_end = sum(days_per_month[0:int(month+1)])
        if (days_up_to_month_end > total_fractional_days):
            mm = month + 1
            if (month > 0):
                full_months_in_days = sum(days_per_month[0:(int(month))])
            break
    print(f"full: {full_months_in_days}")
    fractional_days_remaining = total_fractional_days - full_months_in_days
    dd = math.floor(fractional_days_remaining)

    print(f"month: {mm}, day: {dd}, fract: {fractional_days_remaining-dd}")
    return UTCFractionalDayToJDUTC(yyyy, mm, dd, fractional_days_remaining - dd)    

def UTCFractionalDayToJDUTC(y,m,d, fractional_day):
    return (367 * y - int(7 * (y + int((m + 9)/12))/4) + int(275 * m/9) + d + 1721013.5 + fractional_day)


def GetdATTable():
    return {'57754.0': 37}

# TODO: Update dAT table
# TODO: Pass list of [y, m, d, mm, hh, s] instead of individual floats
# TODO: Other functions
# TODO: check for units [seconds, days, years]
class Time:    
    def __init__(self):
        self.eop_df_ = ConstructEarthObservationParameterTables()
        self.dAT_ = GetdATTable()

    def UTCtoJDUTC(self, y, m, d, hh, mm, ss):
        return (367 * y - int(7 * (y + int((m + 9)/12))/4) + int(275 * m/9) + d + 1721013.5 + ((ss/60 + mm)/60 + hh)/24)
    
    def GregoriantoJSJ2000(self, Gregorian):
        jd = self.UTCtoJDUTC(Gregorian[0], Gregorian[1], Gregorian[2], Gregorian[3], Gregorian[4], Gregorian[5])

        # Julian seconds from J2000 in same frame as 'Gregorian'.
        return ((jd - kJDJ2000) * kDayInSeconds)

    def JSJ2000UTCtoJDUTC(self, js_j2000):
        return (js_j2000/kDayInSeconds) + kJDJ2000
    def MJD(cls, JD):
        return (JD - kMJD_Offset)
    
    def JDtoT(cls, jd):
        return (jd - kJDJ2000)/kCenturyInJulianDays
    
    def GregorianUTCtoJSJ2000UT1(self, y, m, d, hh, mm, ss):
        jd_utc = self.UTCtoJDUTC(y, m, d, hh, mm, ss)
        mjd_utc = self.MJD(jd_utc)
        js_from_j2000_utc = (jd_utc - kJDJ2000) * kDayInSeconds

        dut1_s = self.GetEarthObservationParameter(mjd_utc, 'dUT1_s')
        
        return (js_from_j2000_utc + dut1_s)

    def UTCtoJDTAI(self, y, m, d, hh, mm, ss):
        jd_utc = self.UTCtoJDUTC(y, m, d, hh, mm, ss)
        dat_s = self.GetdATfromGregorian(y, m, d, mm, hh, ss)

        return (jd_utc + dat_s/kDayInSeconds)
    
    def TAIstoTTs(self, tai_s):
        return (tai_s + kdTTs)

    def GregorianUTCtoTTs(cls, y, m, d, hh, mm, ss):
        jd_tai = self.UTCtoTAI(y, m, d, hh, mm, ss)

        return self.TAIstoTTs(jd_tai * kDayInSeconds)

    def UTCtoTUT1(self, y, m, d, hh, mm, ss):
        jd_utc = self.UTCtoJDUTC(y, m, d, hh, mm, ss)
        mjd_utc = self.MJD(jd_utc)
        dut1_s = self.GetEarthObservationParameter(mjd_utc, 'dUT1_s')

        jd_ut1 = jd_utc + dut1_s/kDayInSeconds

        return self.JDtoT(jd_ut1)
    
    def GetdUTfromGregorian(self, y, m, d, hh, mm, ss):
        MJD = self.MJD(self.UTCtoJDUTC(y,m,d,hh,mm,ss))
        return self.GetEarthObservationParameter(MJD, 'dUT1_s')

    def GetEarthObservationParameter(self, mjd, param):
        mjd_lb = math.floor(mjd)
        mjd_ub = math.ceil(mjd)

        lb = pd.to_numeric(self.eop_df_.loc[self.eop_df_['mjd'] == mjd_lb, param])
        ub = pd.to_numeric(self.eop_df_.loc[self.eop_df_['mjd'] == mjd_ub, param])

        return np.interp(mjd, [mjd_lb, mjd_ub], [lb.iloc[0], ub.iloc[0]])

    def GetdATfromGregorian(self, y, m, d, hh, mm, ss):
        MJD = self.MJD(self.UTCtoJDUTC(y,m,d,hh,mm,ss))
        index = [x for x in self.dAT_.keys() if float(x) <= MJD]
        
        return self.dAT_[index[-1]]
