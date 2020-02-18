from ugradio import timing
import numpy as np
import matplotlib.pyplot as plt
import pickle
from ugradio import nch
from rotation import rotate_coords
from power import plot_power


def convert_to_voltage(args):
    if len(a.split('m'))!=2:
        a= a.split('V')*1000
    else:
        a= a.split('m')
    return a/1023


def get_times():
    return  {'local_now' : timing.local_time(),
            'ut_now' : timing.unix_time(), 'julian_now' : timing.julian_date()
            ,'lst_now' : timing.lst()}

def organize_caps(cap, args):
    """
    organize data into a dictionary of lists where the keys are real and imaginary, while each list represents a block of data
    The first 200 samples from each block are removed because of the pico sampler error and the bits are converted to
    voltage (mV) in the process

    """
    # Find conversion from bits to mV
    conversion_factor = convert_to_voltage(args)

    #Remove first 200 samples of each data capture and organize into real and complex
    cap_list_real  = [cap[200+16000*2*N:16000*(2*N+1)]*conversion_factor for N in range(0, args.nblocks)]
    cap_list_image = [cap[200+16000*(2*N+1):16000*2*(N+1)]*conversion_factor for N in range(0, args.nblocks)]

    return {'real': cap_list_real, 'imaginary':cap_list_image}

def set_save(save_file, data):
    # pickle the data to corresponding file
    outfile = open(save_file, 'wb')
    pickle.dump(data,outfile)
    outfile.close()
    print('done saving to: ', save_file)

def get_pos(args, t0):
    """
    Determine position of observation in topocentric, equitorial and galactic coordinates. Only one coordinate combination
    is needed. If none is supplied, this will return none, otherwise return a dictionary with all coordinate references


    """
    if args.ra is not None or args.alt is not None or args.lat is not None:

        if args.ra is not None  and args.dec is not None:
            az, alt = rotate_coords('ra dec->alt az', args.ra, args.dec, t0['lst_now'], args.lat_loc)
            lat, longitude = rotate_coords('ra dec->lat long', args.ra, args.dec, t0['lst_now'], args.lat_loc)
            dec, ra = args.ra, args.dec

        elif args.alt is not None and args.az is not None:
            dec, ra = rotate_coords('alt az->ra dec', args.alt, args.az, t0['lst_now'], args.lat_loc)
            lat, longitude = rotate_coords('alt az->lat long', args.alt, args.az, t0['lst_now'], args.lat_loc)
            az, alt = args.alt, args.az

        elif args.lat is not None and args.longitude is not None:
            dec, ra = rotate_coords('lat long->ra dec', args.lat, args.longitude, t0['lst_now'], args.lat_loc)
            az, alt = rotate_coords('lat long->alt az', args.lat, args.longitude, t0['lst_now'], args.lat_loc)
            lat, longitude = args.lat, args.longitude

        else:
            raise ValueError('Missing either an ALT AZ RA or DEC')
        coord_dict = {'ra':ra, 'dec':dec, 'alt':alt, 'az':az, 'lat':lat, 'long':longitude}

        return coord_dict

    else:
        return

def save(args, cap, t0, tf):
    # Generate file ending with JD naming convention
    file_ending = str(t0['julian_now']).split('.')[0]+'_'+ str(t0['julian_now']).split('.')[1]
    save = False

    # Put the initial and final times into a dictionary
    times = {'initial':t0, 'final':tf}

    # Compute coordintes before and after data capture, store in dict
    coords_0 = get_pos(args, t0)
    coords_f = get_pos(args, tf)
    coords = {'initial': coords_0, 'final':coords_f}

    # Ask if user wants to save the run, if they want a special tag for it and plot the power spectrum
    while save == False:
        save_opt = input('Do you want to save? (y/n): ')

        if save_opt =='y':
            tag = str(input('Add tag? (add tag here or enter n to for no tag): '))

            if tag !='n':
                file_ending = file_ending+'_'+tag

            plot_power(args.path+'/power_plots/plot_'+file_ending, 15800, 62.5e6/args.divisor, cap['real'][0], cap['imaginary'][0])
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
