from ugradio import timing
import numpy as np
import matplotlib.pyplot as plt
import pickle
from ugradio import nch
from rotation import altaz

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

def save(args, cap, t0, tf, ra,dec, alt,az):
    file_ending = str(t0['julian_now']).split('.')[0]+'_'+ str(t0['julian_now']).split('.')[1]
    save = False
    times = {'initial':t0, 'final':tf}
    while save == False:
        save_opt = input('Do you want to save? (y/n): ')
        if save_opt =='y':
            tag = str(input('Add tag? (add tag here or enter n to for no tag): '))
            if tag !='n':
                file_ending = file_ending+'_'+tag

            outfile = open(args.path+'captures/cap_'+file_ending, 'wb')
            pickle.dump(cap,outfile)
            outfile.close()
            print('done saving captures to: '+args.path+'captures/cap_'+file_ending)

            outfile = open(args.path+'/times/time_'+file_ending, 'wb')
            pickle.dump(times,outfile)
            outfile.close()
            print('done saving times to: '+args.path+'/times/time_'+file_ending)

            outfile = open(args.path+'args/arg_'+file_ending, 'wb')
            pickle.dump(args,outfile)
            outfile.close()
            print('done saving args to: '+args.path+'args/arg_'+file_ending)

            if ra or alt:
                if ra is not None  and dec is not None:
                    alt, az = altaz(ra, dec, t0['lst_now'], nch.lat)
                elif alt is not None and az is not None:
                    dec, ra = altaz(alt, az, t0['lst_now'], nch.lat, inverse=True)
                else:
                    raise ValueError('Missing either an ALT AZ RA or DEC')
                coords = {'ra':ra, 'dec':dec, 'alt':alt, 'az':az}
                outfile=open(args.path+'coordinates/coord_'+file_ending, 'wb')
                pickle.dump(coords, outfile)
                print('done saving coords to: '+args.path+'args/arg__'+file_ending)

            save =True
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
