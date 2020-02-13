from ugradio.pico import capture_data as cpd
import numpy as np
import matplotlib.pyplot as plt
from abseil import app, flags
from ugradio import timing
import pickle


FLAGS = flags.FLAGS
flags.DEFINE_string('volt_range', '1V', 'volt range of pico sampler')
flags.DEFINE_string('file_name', 'arr', 'File to save the data too ')
flags.DEFINE_boolean('dual_mode', True, 'to take real and complex data')
flags.DEFINE_integer('divisor', 1, 'divisor for the sampling frequency')
flags.DEFINE_string('path', '/Users/maxlee1993/Documents/Lab_2/, directory to save the data')
flags.DEFINE_integer('n_blocks', 1, 'number of blocks to use')


def main(argv):
    del argv
    cap = cpd(divisor=FLAGS.divisor, volt_range=FLAGS.volt_range, dual_mode=FLAGS.dual_mode, n_blocks=FLAGS.n_blocks)
    #Remove first 200 samples of each data capture
    cap_list = [cap[200+16000*N:16000*(N+1)] for N in range(0, FLAGS.n_bocks) ]


    meta_dict = dict('local_now' = ugradio.timing.local_time(), 'ut_now' = ugradio.timing.unix_time(), 'julian_now' = ugradio.timing.julian_date() ,'lst_now' = ugradio.timing.lst(), 'lst_julian' = ugradio.timing.lst(jd), 'ut_julian' = ugradio.timing.unix_time(jd), 'julian_ut' = ugradio.timing.julian_date(ut))


    #plot out a histogram of one of the blocks,
    plt.figure()
    plt.hist(cap_list[0], bins=1000)
    plt.show()


    save = False
    while save == False:
        save_opt = input('Do you want to save? (y/n): ')
        if save_opt =='y':
            outfile = open(path+file_name, 'wb')
            pickle.dump(cap_list,outfile)
            outfile.close()

            outfile = open(path+file_name+'_meta_dict', 'wb')
            pickle.dump(meta_dict,outfile)
            outfile.close()
            print('done saving to: '+path+file_name)
            save =True
        elif:
            save_opt=='n':
                return -1
        else:
            print('choose y or n')


if __name__ == '__main__':
    app.run(main)

