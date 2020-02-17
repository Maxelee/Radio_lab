import numpy as np
import pdb

def convert_ra(ra):
    try:
        sign_ra, value_ra= ra.split('-')
    except:
        sign_ra= None
        value_ra=ra
    if sign_ra =='':
        h, m, s = value_ra.split(':')
        ra = -(int(h)+int(m)/60+int(s)/3600)*np.pi/12
    else:
        h, m, s = ra.split(':')
        ra =  (int(h) + int(m)/60+int(s)/3600)*np.pi/12
    return ra

def convert_dec(dec):
    try:
        sign_dec, value_dec= dec.split('-')
    except:
        sign_dec = None
        value_dec=dec
    if sign_dec =='':
        d, m, s = value_dec.split(':')
        dec =-(int(d)+int(m)/60+int(s)/3600)*np.pi/180
    else:
        d, m, s = dec.split(':')
        dec =  (int(d) + int(m)/60+int(s)/3600)*np.pi/180
    return dec

def get_spherical_coord(coord_1, coord_2):
    return np.array([
        np.cos(coord_1)*np.sin(coord_2),
        np.sin(coord_1)*np.sin(coord_2),
        np.cos(coord_2)])

def swap_y():
    return np.array([
        [1, 0, 0],
        [0,-1, 0],
        [0, 0, 1]])


def eq_eqc(lst):
    return np.array([
        [np.cos(lst), np.sin(lst),  0],
        [-np.sin(lst), np.cos(lst), 0],
        [0,               0,        1]])


def eq_top(lat):
    return np.array([
        [-np.sin(lat), 0, np.cos(lat)],
        [0,           -1,           0],
        [np.cos(lat), 0, np.sin(lat)]])

def eqc_gal():
    return np.array([
        [-.054876, -.873437, -.483835],
        [.494109,  -.444830,  .746982],
        [-.867666, -.198076, .455984]])


def radec_hadec(lst, inverse=False):
    R_2 = swap_y()
    R_1 = eq_eqc(lst)
    if not inverse:
        return np.dot(R_2, R_1)
    else:
        return np.dot(R_2, R_1).T

def hadec_altaz(lat, inverse=False):
    R = eq_top(lat*np.pi/180)
    if not inverse:
        return R
    else:
        return R.T

def radec_latlong(lst, inverse=False):
    R_1 = eq_eqc(lst)
    R_2 = eqc_gal()
    if not inverse:
        return np.dot(R_2, R_1)
    else:
        return np.dot(R_2, R_1).T



def rotate_coords(transform_type, coord_1, coord_2, lst, lat):
    """
    Convert from right ascension and declination to altitude and azimuth

    Paramaters
    ____________________________________________________________________
    transform_type: determine direction of transformation
    alt az->ra dec, ra dec->alt az, lat long->ra dec, ra dec->lat long,
    lat long->alt az, alt az->lat long
    coord_1: altitude, right ascension or galactic latitude
    coord_2: azimuth, declination, or galactic longitude
    lst: in hours
    latitude: latitude in degrees
    Returns
    ___________________________________________________________________
    returns output of transform type
    """

    if transform_type   == 'alt az->ra dec':
        alt_az_vec = get_spherical_coord(coord_2, coord_1)
        rotation_1 = hadec_altaz(lat, inverse=True)
        rotation_2 = radec_hadec(lst, inverse=True)
        converted_vec =  np.dot(rotation_2,np.dot( rotation_1, alt_az_vec))

    elif transform_type == 'ra dec->alt az':
        try:
            ra = float(coord_1)
            dec= float(coord_2)
        except:
            ra = convert_ra(coord_1)
            dec = convert_dec(coord_2)

        ra_dec_vec = get_spherical_coord(dec, ra)
        rotation_2 = hadec_altaz(lat, inverse=False)
        rotation_1 = radec_hadec(lst, inverse=False)
        converted_vec =  np.dot(rotation_2,np.dot(rotation_1,ra_dec_vec))

    elif transform_type == 'ra dec->lat long':
        try:
            ra = float(coord_1)
            dec= float(coord_2)
        except:
            ra = convert_ra(coord_1)
            dec = convert_dec(coord_2)

        ra_dec_vec = get_spherical_coord(dec, ra)
        rotation_1 = radec_latlong(lst, inverse=False)
        converted_vec =  np.dot(rotation_1, ra_dec_vec)

    elif transform_type == 'lat long->ra dec':
        lat_long_vec = get_spherical_coords(coord_1, coord_2)
        rotation_1 = radec_latlong(lst, inverse=True)
        converted_vec = np.dot(rotation_1, lat_long_vec)
    elif transform_type == 'lat long->alt az':
        lat_long_vec = get_spherical_coords(coord_1, coord_2)
        rotation_1 = radec_latlong(lst, inverse=True)
        rotation_2 = radec_hadec(lst, inverse=False)
        rotation_3 = hadec_altaz(lat, inverse=False)
        converted_vec = np.dot(rotation_3, np.dot(rotation_2, np.dot(rotation_1, lat_long_vec)))

    elif transform_type == 'alt az->lat long':
        alt_az_vec = get_spherical_coords(coord_2, coord_1)
        rotation_3 = radec_latlong(lst, inverse=False)
        rotation_2 = radec_hadec(lst, inverse=True)
        rotation_1 = hadec_altaz(lat, inverse=True)
        converted_vec = np.dot(rotation_3, np.dot(rotation_2, np.dot(rotation_1, lat_long_vec)))

    else:
        raise ValueError('Transformation options are only: alt az->ra dec, ra dec->alt az,ra dec->lat long,lat long->ra dec, alt az->lat long, lat long->alt az')

    new_coord_1 = np.arcsin(converted_vec[2])
    new_coord_2 = np.arctan2(converted_vec[0], converted_vec[1])

    return new_coord_1*180/np.pi, new_coord_2*180/np.pi


