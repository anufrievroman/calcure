"""Module that controls display of the moon phases"""

from math import cos, floor, fmod, modf, radians, sin


"""Most all equations are taken from the book Astronomical Algorithms,
   2nd Ed., by Jean Meeus, 1998.  """


def jd2ymd(jd: float) -> (int, int, float):
    """Converts the given Julian day number to the
    Gregorian year, month and day.

    The day is a float which represents the day and
    fraction of a day.
    For example, day = 1.5 would be 12 noon on the
    first day.

    Calculation follows pg. 63 of Astronomical Algorithms.
    No equation numbers given in text.  From Example 7.c:

    JD 2436116.31 => 1957 October 4.81

    """
    jd_plus = jd + 0.5
    F, Z = modf(jd_plus)
    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - int(alpha / 4)
    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)
    day = B - D - int(30.6001 * E) + F
    if E < 14:
        month = E - 1
    else:
        month = E - 13
    if month > 2:
        year = C - 4716
    else:
        year = C - 4715

    return year, month, day


def delta_t(year: int) -> float:
    """Calculate the difference between Universal Time and
    Dynamic Time i.e., delta_t = Dynamic Time - Universal Time.
    The return value is in units of days.

    Using equations from NASA website:
    https://eclipse.gsfc.nasa.gov/SEhelp/deltatpoly2004.html
    Note this is a polynomial approximation.
    """
    if year > 2005 and year < 2050:
        t = year - 2000
        delta_t = 62.92 + 0.32217 * t + 0.005589 * t**2
    elif year >= 2050 and year < 2150:
        delta_t = -20 + 32 * ((year - 1820) / 100) ** 2 - 0.5628 * (2150 - year)
    else:
        delta_t = 0

    delta_t = delta_t / (60 * 60 * 24)  # Convert from seconds to days

    return delta_t


def is_divisible_by(dividend, divisor):
    """Determine if the given dividend is divisible (integer
    divivion) by the given divisor (without remainder).
    """
    return dividend / divisor == int(dividend / divisor)


def is_leap_year(year: int) -> bool:
    """Determine if the given year (Gregorian calendar)
    is a leap year or not.

    Calculation follows information given on pg. 62 of
    Astronomical Algorithms, in the box.  No equation
    numbers in text.
    """
    if is_divisible_by(year, 100):
        return is_divisible_by(year, 400):
    return is_divisible_by(year, 4):


def major_correction(k: float, T: float, phase: str) -> float:
    """Calculation of the large correction to the Julian Day
    obtained by Eq. 49.3.  The return value is in units of
    days.

    See pgs. 350 - 352 of Astronomical Algorithms.
    """
    E = 1.0 - 0.002516 * T - 0.000_007_4 * T**2  # Eq. 47.6
    M = (
        2.5534 + 29.105_356_7 * k - 0.000_001_4 * T**2 - 0.000_000_11 * T**3
    )  # Eq. 49.4, units: deg.
    M = fmod(M, 360)
    if M < 0:
        M += 360
    M = radians(M)
    M_prime = (
        201.5643
        + 385.816_935_28 * k
        + 0.010_758_2 * T**2
        + 0.000_012_38 * T**3
        - 0.000_000_058 * T**4
    )  # Eq. 49.5, units: deg.
    M_prime = fmod(M_prime, 360)
    if M_prime < 0:
        M_prime += 360
    M_prime = radians(M_prime)
    F = (
        160.7108
        + 390.670_502_84 * k
        - 0.001_611_8 * T**2
        - 0.000_002_27 * T**3
        + 0.000_000_011 * T**4
    )  # Eq. 49.6, units: deg
    F = fmod(F, 360)
    if F < 0:
        F += 360
    F = radians(F)
    Omega = (
        124.7746 - 1.563_755_88 * k + 0.002_067_2 * T**2 + 0.000_002_15 * T**3
    )  # Eq. 49.7, units: deg
    Omega = fmod(Omega, 360)
    if Omega < 0:
        Omega += 360
    Omega = radians(Omega)
    if phase == "New Moon":
        coeff = [
            -0.40720,
            0.17241,
            0.01608,
            0.01039,
            0.00739,
            -0.00514,
            0.00208,
            -0.00111,
            -0.00057,
            0.00056,
            -0.00042,
            0.00042,
            0.00038,
            -0.00024,
            -0.00017,
            -0.00007,
            0.00004,
            0.00004,
            0.00003,
            0.00003,
            -0.00003,
            0.00003,
            -0.00002,
            -0.00002,
            0.00002,
        ]
    if phase == "Full Moon":
        coeff = [
            -0.40614,
            0.17302,
            0.01614,
            0.01043,
            0.00734,
            -0.00515,
            0.00209,
            -0.00111,
            -0.00057,
            0.00056,
            -0.00042,
            0.00042,
            0.00038,
            -0.00024,
            -0.00017,
            -0.00007,
            0.00004,
            0.00004,
            0.00003,
            0.00003,
            -0.00003,
            0.00003,
            -0.00002,
            -0.00002,
            0.00002,
        ]
    if phase == "New Moon" or phase == "Full Moon":
        corr = (
            coeff[0] * sin(M_prime)
            + coeff[1] * E * sin(M)
            + coeff[2] * sin(2 * M_prime)
            + coeff[3] * sin(2 * F)
            + coeff[4] * E * sin(M_prime - M)
            + coeff[5] * E * sin(M_prime + M)
            + coeff[6] * E**2 * sin(2 * M)
            + coeff[7] * sin(M_prime - 2 * F)
            + coeff[8] * sin(M_prime + 2 * F)
            + coeff[9] * E * sin(2 * M_prime + M)
            + coeff[10] * sin(3 * M_prime)
            + coeff[11] * E * sin(M + 2 * F)
            + coeff[12] * E * sin(M - 2 * F)
            + coeff[13] * E * sin(2 * M_prime - M)
            + coeff[14] * sin(Omega)
            + coeff[15] * sin(M_prime + 2 * M)
            + coeff[16] * sin(2 * M_prime - 2 * F)
            + coeff[17] * sin(3 * M)
            + coeff[18] * sin(M_prime + M - 2 * F)
            + coeff[19] * sin(2 * M_prime + 2 * F)
            + coeff[20] * sin(M_prime + M + 2 * F)
            + coeff[21] * sin(M_prime - M + 2 * F)
            + coeff[22] * sin(M_prime - M - 2 * F)
            + coeff[23] * sin(3 * M_prime + M)
            + coeff[24] * sin(4 * M_prime)
        )
    if phase == "First Quarter" or phase == "Last Quarter":
        coeff = [
            -0.62801,
            0.17172,
            -0.01183,
            0.00862,
            0.00804,
            0.00454,
            0.00204,
            -0.00180,
            -0.00070,
            -0.00040,
            -0.00034,
            0.00032,
            0.00032,
            -0.00028,
            0.00027,
            -0.00017,
            -0.00005,
            0.00004,
            -0.00004,
            0.00004,
            0.00003,
            0.00003,
            0.00002,
            0.00002,
            -0.00002,
        ]
        corr = (
            coeff[0] * sin(M_prime)
            + coeff[1] * E * sin(M)
            + coeff[2] * E * sin(M_prime + M)
            + coeff[3] * sin(2 * M_prime)
            + coeff[4] * sin(2 * F)
            + coeff[5] * E * sin(M_prime - M)
            + coeff[6] * E**2 * sin(2 * M)
            + coeff[7] * sin(M_prime - 2 * F)
            + coeff[8] * sin(M_prime + 2 * F)
            + coeff[9] * sin(3 * M_prime)
            + coeff[10] * E * sin(2 * M_prime - M)
            + coeff[11] * E * sin(M + 2 * F)
            + coeff[12] * E * sin(M - 2 * F)
            + coeff[13] * E**2 * sin(M_prime + 2 * M)
            + coeff[14] * E * sin(2 * M_prime + M)
            + coeff[15] * sin(Omega)
            + coeff[16] * sin(M_prime - M - 2 * F)
            + coeff[17] * sin(2 * M_prime + 2 * F)
            + coeff[18] * sin(M_prime + M + 2 * F)
            + coeff[19] * sin(M_prime - 2 * M)
            + coeff[20] * sin(M_prime + M - 2 * F)
            + coeff[21] * sin(3 * M)
            + coeff[22] * sin(2 * M_prime - 2 * F)
            + coeff[23] * sin(M_prime - M + 2 * F)
            + coeff[24] * sin(3 * M_prime + M)
        )
        W = (
            0.00306
            - 0.00038 * E * cos(M)
            + 0.00026 * cos(M_prime)
            - 0.00002 * cos(M_prime - M)
            + 0.00002 * cos(M_prime + M)
            + 0.00002 * cos(2 * F)
        )
        if phase == "First Quarter":
            corr += W
        elif phase == "Last Quarter":
            corr -= W

    return corr


def minor_correction(k: float, T: float) -> float:
    """The small correction to the Julian Day calculated
    using Eq. 49.3.  The return value is in units of days.

    See pgs. 351 - 352 of Astronomical Algorithms.
    """
    a1 = 299.77 + 0.107408 * k - 0.009173 * T**2
    a2 = 251.88 + 0.016321 * k
    a3 = 251.83 + 26.651886 * k
    a4 = 349.42 + 36.412478 * k
    a5 = 84.66 + 18.206239 * k
    a6 = 141.74 + 53.303771 * k
    a7 = 207.14 + 2.453732 * k
    a8 = 154.84 + 7.306860 * k
    a9 = 34.52 + 27.261239 * k
    a10 = 207.19 + 0.121824 * k
    a11 = 291.34 + 1.844379 * k
    a12 = 161.72 + 24.198154 * k
    a13 = 239.56 + 25.513099 * k
    a14 = 331.55 + 3.592518 * k

    a1 = radians(fmod(a1, 360))
    a2 = radians(fmod(a2, 360))
    a3 = radians(fmod(a3, 360))
    a4 = radians(fmod(a4, 360))
    a5 = radians(fmod(a5, 360))
    a6 = radians(fmod(a6, 360))
    a7 = radians(fmod(a7, 360))
    a8 = radians(fmod(a8, 360))
    a9 = radians(fmod(a9, 360))
    a10 = radians(fmod(a10, 360))
    a11 = radians(fmod(a11, 360))
    a12 = radians(fmod(a12, 360))
    a13 = radians(fmod(a13, 360))
    a14 = radians(fmod(a14, 360))

    corr = (
        325 * sin(a1)
        + 165 * sin(a2)
        + 164 * sin(a3)
        + 126 * sin(a4)
        + 110 * sin(a5)
        + 62 * sin(a6)
        + 60 * sin(a7)
        + 56 * sin(a8)
        + 47 * sin(a9)
        + 42 * sin(a10)
        + 40 * sin(a11)
        + 37 * sin(a12)
        + 35 * sin(a13)
        + 23 * sin(a14)
    )
    corr = 1e-6 * corr

    return corr


def get_moon_phase(year: int, month: int, day: int) -> str:
    rval = ""
    if month in [1, 3, 5, 7, 8, 10, 12]:
        days_in_month = 31
    elif month in [4, 6, 9, 11]:
        days_in_month = 30
    else:
        if is_leap_year(year):
            days_in_month = 29
        else:
            days_in_month = 28
    year_dec = (
        year + (month - 1) / 12 + (day - 1) / (days_in_month * 12)
    )  # convert given year, month, and day to year with decimal
    k = (year_dec - 2000) * 12.3685  # Eq. 49.2
    k_new = floor(k)
    for i, k_val in enumerate([k_new, k_new + 0.25, k_new + 0.5, k_new + 0.75]):
        T = k_val / 1236.85  # Eq. 49.3
        jde_val = (
            2451550.09766
            + 29.530588861 * k_val
            + 0.00015437 * T**2
            - 0.00000015 * T**3
            + 0.000_000_000_73 * T**4
        )  # Eq. 49.1, units: days
        if i == 0:
            jde_val = (
                jde_val
                + major_correction(k_val, T, "New Moon")
                + minor_correction(k_val, T)
                - delta_t(year)
            )
        elif i == 1:
            jde_val = (
                jde_val
                + major_correction(k_val, T, "First Quarter")
                + minor_correction(k_val, T)
                - delta_t(year)
            )
        elif i == 2:
            jde_val = (
                jde_val
                + major_correction(k_val, T, "Full Moon")
                + minor_correction(k_val, T)
                - delta_t(year)
            )
        elif i == 3:
            jde_val = (
                jde_val
                + major_correction(k_val, T, "Last Quarter")
                + minor_correction(k_val, T)
                - delta_t(year)
            )
        calc_year, calc_month, calc_day = jd2ymd(jde_val)
        calc_day = int(calc_day)

        if (calc_year, calc_month, calc_day) == (year, month, day):
            if i == 0:
                rval = " 🌑"  # New Moon
            if i == 1:
                rval = " 🌓"  # First Quarter
            if i == 2:
                rval = " 🌕"  # Full Moon
            if i == 3:
                rval = " 🌗"  # Last Quarter
    return rval
