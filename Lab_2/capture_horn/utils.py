from ugradio import timing
import numpy as np
import matplotlib.pyplot as plt
import pickle
from ugradio import nch
from rotation import rotate_coords
from power import plot_power
import os
from average import power_mean
def convert_to_voltage(args):
    volt_range = args.volt_range
    if len(volt_range.split('m'))!=2:
        factor= float(volt_rage.split('V')[0]*1000)
    else:
        factor= float(volt_range.split('m')[0])
    return factor/1023


def get_times():
    return  {'local' : timing.local_time(),
            'ut' : timing.unix_time(), 'julian' : timing.julian_date()
            ,'lst' : timing.lst()}

def organize_caps(cap, args):
    """
    organize data into a dictionary of lists where the keys are real and imaginary, while each list represents a block of data
    The first 200 samples from each block are removed because of the pico sampler error and the bits are converted to
    voltage (mV) in the process

    """
    # Find conversion from bits to mV
    conversion_factor = convert_to_voltage(args)

    #Remove first 200 samples of each data capture and organize into real and complex
    if args.iterations is None:
        sample_len = args.nblocks

    else:
        sample_len = args.nblocks*args.iterations

    #Drop the first 200 samples and seperate real from imaginary components
    cap_list_real  = [cap[200+16000*2*N:16000*(2*N+1)]*conversion_factor for N in range(sample_len)]
    cap_list_image = [cap[200+16000*(2*N+1):16000*2*(N+1)]*conversion_factor for N in range(sample_len)]

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
            az, alt = rotate_coords('ra dec->alt az', args.ra, args.dec, t0['lst'], args.lat_loc)
            lat, longitude = rotate_coords('ra dec->lat long', args.ra, args.dec, t0['lst'], args.lat_loc)
            dec, ra = args.ra, args.dec

        elif args.alt is not None and args.az is not None:
            dec, ra = rotate_coords('alt az->ra dec', args.alt, args.az, t0['lst'], args.lat_loc)
            lat, longitude = rotate_coords('alt az->lat long', args.alt, args.az, t0['lst'], args.lat_loc)
            az, alt = args.alt, args.az

        elif args.lat is not None and args.longitude is not None:
            dec, ra = rotate_coords('lat long->ra dec', args.lat, args.longitude, t0['lst'], args.lat_loc)
            az, alt = rotate_coords('lat long->alt az', args.lat, args.longitude, t0['lst'], args.lat_loc)
            lat, longitude = args.lat, args.longitude

        else:
            raise ValueError('Missing either an ALT AZ RA or DEC')
        coord_dict = {'ra':ra, 'dec':dec, 'alt':alt, 'az':az, 'lat':lat, 'long':longitude}

        return coord_dict

    else:
        return

def save(args, cap, t0, tf):
    # Generate file ending and folder with JD naming convention
    folder, file_ending = str(tf['julian']).split('.')[0], str(round(tf['lst'], 2)).split('.')[0]+'-'+str(round(tf['lst'], 2)).split('.')[1]
    save = False

    # Put the initial and final times into a dictionary
    times = {'initial':t0, 'final':tf}

    # Compute coordintes before and after data capture, store in dict
    coords_0 = get_pos(args, t0)
    coords_f = get_pos(args, tf)
    coords = {'initial': coords_0, 'final':coords_f}
    caps_arr = np.asarray(cap['real'])+1.0j*np.asarray(cap['imaginary'])
    power  = power_mean(args,caps_arr)

    # Ask if user wants to save the run, if they want a special tag for it and plot the power spectrum
    while not save:
        save_opt = input('do you want to save? (y/n): ')

        #Add a special tag to the data capturing
        if save_opt =='y':
            tag = input('do you want to enter a tag? (n for none): ')

            if tag !='n':
                file_ending = file_ending+'_'+tag

            try:
                os.mkdir(args.path +  'captures/'    +  folder)
                os.mkdir(args.path +  'times/'       +  folder)
                os.mkdir(args.path +  'args/'        +  folder)
                os.mkdir(args.path +  'coordinates/' +  folder)
                os.mkdir(args.path +  'power/'       +  folder)
            except FileExistsError:
                print('folders for today already exist')

            set_save(args.path+'captures/' + folder +  '/cap_'  +   file_ending, cap)
            set_save(args.path+'times/'    + folder +  '/time_'  +  file_ending, times)
            set_save(args.path+'args/'     + folder +  '/arg_'   +  file_ending, args)
            set_save(args.path+'power/'    + folder +  '/power_'   +  file_ending, args)

            if coords is not None:
                set_save(args.path+'coordinates/' + folder + '/coord_'+file_ending, coords)

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
