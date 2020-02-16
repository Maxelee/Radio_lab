from ugradio import timing
import numpy as np
import matplotlib.pyplot as plt
import pickle
from ugradio import nch
from rotation import rotate_coords

def get_times():
    return  {'local_now' : timing.local_time(),
            'ut_now' : timing.unix_time(), 'julian_now' : timing.julian_date()
            ,'lst_now' : timing.lst()}

def organize_caps(cap, args):

    #Remove first 200 samples of each data capture and organize into real and complex
    cap_list_real  = [cap[200+16000*2*N:16000*(2*N+1)] for N in range(0, args.nblocks)]
    cap_list_image = [cap[200+16000*(2*N+1):16000*2*(N+1)] for N in range(0, args.nblocks)]
    cap = {'real': cap_list_real, 'imaginary':cap_list_image}

    return cap
def set_save(save_file, data):

    outfile = open(save_file, 'wb')
    pickle.dump(data,outfile)
    outfile.close()
    print('done saving to: ', save_file)

def get_pos(args, t0):
    if args.ra or args.alt or args.lat:

        if args.ra is not None  and args.dec is not None:
            alt, az = rotate_coords('ra dec->alt az', args.ra, args.dec, t0['lst_now'], nch.lat)
            lat, longitude = rotate_coords('ra dec->lat long', args.ra, args.dec, t0['lst_now'], nch.lat)
            ra, dec = args.ra, args.dec
        elif args.alt is not None and args.az is not None:
            ra, dec = rotate_coords('alt az->ra dec', args.alt, args.az, t0['lst_now'], nch.lat)
            lat, longitude = rotate_coords('alt az->lat long', args.alt, args.az, t0['lst_now'], nch.lat)
            alt, az = args.alt, args.az
        elif args.lat is not None and args.longitude is not None:
            ra, dec = rotate_coords('lat long->ra dec', args.lat, args.longitude, t0['lst_now'], nch.lat)
            alt, az = rotate_coords('lat long->alt az', args.lat, args.longitude, t0['lst_now'], nch.lat)
            lat, longitude = args.lat, args.longitude
        else:
            raise ValueError('Missing either an ALT AZ RA or DEC')

        return {'ra':ra, 'dec':dec, 'alt':alt, 'az':az, 'lat':lat, 'long':longitude}
    else:
        return

def save(args, cap, t0, tf):
    file_ending = str(t0['julian_now']).split('.')[0]+'_'+ str(t0['julian_now']).split('.')[1]
    save = False
    times = {'initial':t0, 'final':tf}
    coords = get_pos(args, t0)
    while save == False:
        save_opt = input('Do you want to save? (y/n): ')
        if save_opt =='y':
            tag = str(input('Add tag? (add tag here or enter n to for no tag): '))
            if tag !='n':
                file_ending = file_ending+'_'+tag
            set_save(args.path+'captures/cap_'+file_ending, cap)
            set_save(args.path+'/times/time_'+file_ending, times)
            set_save(args.path+'args/arg_'+file_ending, args)
            if coords is not None:
                set_save(args.path+'coordinates/coord_'+file_ending, coords)
            save = True
        elif save_opt=='n':
                return -1
        else:
            print('choose y or n')

def test_hist(cap):
    plt.figure()
    plt.hist(cap['real'][0], bins=100)
    #plot out a histogram of one of the blocks,
    # fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True, gridspec_kw={'hspace':0})
    # ax1.hist(cap['real'][0], bins=100)
    # ax2.hist(cap['imaginary'][0], bins=100)
    plt.show()
