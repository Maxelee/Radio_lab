import numpy as np

def convert_ra(ra):
    h, m, s = ra.split(':')
    return (int(h) + int(m)/60+int(s)/3600)*np.pi/12

def convert_dec(dec):
    d, m, s = dec.split(':')
    return int(d)+int(m)/60+int(s)/3600

def ra_dec_eq(ra, dec):
    return np.array([np.cos(ra)*np.sin(dec), np.sin(ra)*np.cos(dec), np.sin(dec)])

def alt_az_eq(alt, az):
    return np.array([np.cos(az)*np.cos(alt), np.sin(az)*np.cos(alt), np.sin(alt)])

def HA(R):
    swap_matrix = np.array([[1,0,0],[0,-1,0],[0,0,1]])
    return np.einsum('ij, ij->ij', swap_matrix, R)

def eq_eqc(lst):
    R =  np.array([[np.cos(lst), np.sin(lst), 0],[-np.sin(lst), np.cos(lst), 0],[0,0,1]])
    return HA(R)

def eq_top(lat):
    return np.array([[-np.sin(lat), 0, np.cos(lat)],[0,-1,0],[np.cos(lat), 0, np.sin(lat)]])

def eqc_top(coord_1, coord_2, lst, lat, inverse=False):
    if not inverse:
        try:
            test =ra/3
        except:
            ra = convert_ra(coord_1)

        try:
            test =dec/3
        except:
            dec = convert_dec(coord_2)

    lst *= np.pi/12
    lat *= np.pi/180
    if not inverse:
        return np.dot(np.dot(eq_eqc(lst), eq_top(lat)), ra_dec_eq(ra, dec))
    else:
        alt = coord_1*np.pi/180
        az  = coord_2*np.pi/180
        return np.dot(np.dot(eq_eqc(lst), eq_top(lat)).T, alt_az_eq(alt,az))
def altaz(coord_1, coord_2, lst, lat, inverse=False):
    """
    Convert from right ascension and declination to altitude and azimuth

    Paramaters
    ____________________________________________________________________
    coord_1: float of alt in degrees or string  of right ascension in hours minutes seconds or float in radian
    dec: float of alt in degrees or string of declination in degrees minutes seconds or float in radian
    lst: in hours

    Returns
    ___________________________________________________________________
    altitude and azimuth vector
    """
    converted_vec = eqc_top(coord_1, coord_2, lst, lat, inverse=inverse)
    alt_or_dec = np.arcsin(converted_vec[-1])
    az_or_ra = np.arctan2(converted_vec[0], converted_vec[1])
    return alt_or_dec, az_or_ra





