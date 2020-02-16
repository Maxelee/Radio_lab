import numpy as np

def convert_ra(ra):
    h, m, s = ra.split(':')
    return (int(h) + int(m)/60+int(s)/3600)*np.pi/12

def convert_dec(dec):
    d, m, s = dec.split(':')
    return int(d)+int(m)/60+int(s)/3600

def get_spherical_coord(coord_1, coord_2):
    return np.array([np.cos(coord_1)*np.sin(coord_2), np.sin(coord_1)*np.cos(coord_2), np.sin(coord_2)])

def HA(R):
    swap_matrix = np.array([[1,0,0],[0,-1,0],[0,0,1]])
    return np.einsum('ij, ij->ij', swap_matrix, R)

def eq_eqc(lst):
    R =  np.array([[np.cos(lst), np.sin(lst), 0],[-np.sin(lst), np.cos(lst), 0],[0,0,1]])
    return HA(R)

def eq_top(lat):
    return np.array([[-np.sin(lat), 0, np.cos(lat)],[0,-1,0],[np.cos(lat), 0, np.sin(lat)]])

def eqc_gal():
    return np.array([[-.054876, -.873437, -.483835],[.494109, -.444830, .746982],[-.867666, -.198076, .455984]])

def altaz_radec(coord_1, coord_2, lst, lat, inverse=False):
    if not inverse:
        try:
            test =coord_1/3
        except:
            coord_1 = convert_ra(coord_1)

        try:
            test =coord_2/3
        except:
            coord_2 = convert_dec(coord_2)

    lst *= np.pi/12
    lat *= np.pi/180
    if not inverse:
        # return altitude and azimuth vector
        return np.dot(np.dot(eq_eqc(lst), eq_top(lat)), get_spherical_coord(coord_1, coord_2))

    else:
        alt = coord_1*np.pi/180
        az  = coord_2*np.pi/180
        # return right ascension and declination vector
        return np.dot(np.dot(eq_eqc(lst), eq_top(lat)).T,get_spherical_coord(alt,az) )

def radec_latlong(coord_1, coord_2, lst, lat, inverse=False):
    if not inverse:
        try:
            test =coord_1/3
        except:
            coord_1 = convert_ra(coord_1)

        try:
            test =coord_2/3
        except:
            coord_1 = convert_dec(coord_2)

    lst *= np.pi/12
    lat *= np.pi/180
    if not inverse:
        # return lat and long vector
        return np.dot(np.dot(eqc_gal(), HA(eq_eqc(lst))), get_spherical_coord(coord_1, coord_2))
    else:
        lat = coord_1*np.pi/180
        longitude= coord_2*np.pi/180
        # return ra and dec
        return np.dot(np.dot(eqc_gal(), HA(eq_eqc(lst))).T, get_spherical_coord(lat, longitude))



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
        converted_vec = altaz_radec(coord_1, coord_2, lst, lat, inverse=False)
    elif transform_type == 'ra dec->alt az':
        converted_vec =  altaz_radec(coord_1, coord_2, lst, lat, inverse=True)
    elif transform_type == 'ra dec->lat long':
        converted_vec =  radec_latlong(coord_1, coord_2, lst, lat, inverse=False)
    elif transform_type == 'lat long->ra dec':
        converted_vec =  radec_latlong(coord_1, coord_2, lst, lat, inverse=True)
    elif transform_type == 'lat long->alt az':
        converted_vec =  radec_latlong(coord_1, coord_2, lst, lat, inverse=True)
        dec = np.arcsin(converted_vec[-1])
        ra  = np.arctan2(converted_vec[0], converted_vec[1])
        converted_vec =  altaz_radec(ra,dec, lst, lat, inverse=True)
    elif transform_type == 'alt az->lat long':
        converted_vec = altaz_radec(coord_1, coord_2, lst, lat, inverse=False)
        alt = np.arcsin(converted_vec[-1])
        az  = np.arctan2(converted_vec[0], converted_vec[1])
        converted_vec =  radec_latlong(alt,az, lst, lat, inverse=False)
    else:
        raise ValueError('Transformation options are only: alt az->ra dec, ra dec->alt az,ra dec->lat long,lat long->ra dec, alt az->lat long, lat long->alt az')

    coord_1 = np.arcsin(converted_vec[-1])
    coord_2 = np.arctan2(converted_vec[0], converted_vec[1])

    return coord_1, coord_2
