import numpy as np
from ugradio import interf, coord, timing, nch
from time import sleep
import argparse
import os
import sources

my_parser = argparse.ArgumentParser(description='Move the interf.')

my_parser.add_argument('--path',metavar='path', type=str, default='/home/maxlee1993/Documents/radio_lab/Radio_lab/Lab_3/data/tracking',help=' directory to save the data')
my_parser.add_argument('--sleep_time', metavar='sleep_time', type=int, default=30, help='seconds to wait before moving')
my_parser.add_argument('--moon_track', metavar='moon_track', type=bool, default=False, help='for moon tracking')
my_parser.add_argument('--sun_track', metavar='sun_track', type=bool, default=False, help='for sun tracking')
my_parser.add_argument('--source', metavar='source', type=str, help='point source for observation')
args = my_parser.parse_args()

def main():
    ################ ORGANIZING FILES AND DIRECTORIES #############
    # Check if the JD exists
    JD = timing.julian_date()
    path = args.path + '/' + str(round(int(JD)))
    path_exists = os.path.exists(path)
    if path_exists:
        pass
    else:
        os.mkdir(path)
    # Make some empty lists to add to
    alts = []
    azs  = []
    lsts = []
    # bring in source information
    source_dict = {source.name: source for source in sources.sources}
    lat, lon, alt = nch.lat, nch.lon, nch.alt
    ifm = interf.Interferometer()
    pointing_good=True
    try:
        while pointing_good:
            JD = timing.julian_date()
            if args.sun_track:
                ra, dec = coord.sunpos(JD)
            elif args.moon_track:
                ra, dec = coord.moonpos(JD)
            else:
                assert args.source in source_dict, "choose, crab cygnus M17 orion or cas"
                ra, dec = source_dict[args.source].ra, source_dict[args.source].dec
            alt, az = coord.get_altaz(ra, dec, JD, lat, lon, alt)
            if az <= 90:
                az +=180
                alt =(180- alt)
            if az >= 300:
                az -= 180
                alt=(180 - alt)

            #store time and location
            lsts.append(timing.lst())
            alts.append(alt)
            azs.append(az)
            #point at source
            print(alt, az)
            ifm.point(alt, az)
            print('pointing to {} at alt:{}, az:{}'.format(args.source, alt, az))
            #wait 1 minute
            sleep(args.sleep_time)
    except KeyboardInterrupt:
        #Save alts and azs
        np.savez(path+'/time_and_coords', alts=alts, azs=azs, lsts=lsts)

        ifm.stow()

    finally:    #Save alts and azs
        print('ERROR')
        np.savez(path+'/time_and_coords', alts=alts, azs=azs, lsts=lsts)

        ifm.stow()

if __name__=='__main__':
    main()
