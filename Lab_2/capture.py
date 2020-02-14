from ugradio.pico import capture_data as cpd
import numpy as np
import matplotlib.pyplot as plt
from ugradio import timing
import pickle
import argparse



def main():
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--volt_range',metavar='volt_range', type=str, default='1V',help='volt range of pico sampler')
    parser.add_argument('--file_name', metavar='file_name', type=str, default='arr',help= 'File to save the data too ')
    parser.add_argument('--dual_mode',metavar='dual_mode', type=bool, default= False, help='to take real and complex data')
    parser.add_argument('--divisor', metavar='divisor', type=int,default=1, help='divisor for the sampling frequency')
    parser.add_argument('--path',metavar='path', type=str, default='/Users/maxlee1993/Documents/Lab_2/',help=' directory to save the data')
    parser.add_argument('--nblocks',metavar='nblocks', type=int, default=1, help='number of blocks to use')
    args=parser.parse_args()

    meta_dict_initial : {'local_now' : ugradio.timing.local_time(), 'ut_now' : ugradio.timing.unix_time(), 'julian_now' : ugradio.timing.julian_date() ,'lst_now' : ugradio.timing.lst()}
    cap = cpd(divisor=args.divisor, volt_range=args.volt_range, dual_mode=args.dual_mode, nblocks=args.nblocks)
   


    meta_dict_final : {'local_now' : ugradio.timing.local_time(), 'ut_now' : ugradio.timing.unix_time(), 'julian_now' : ugradio.timing.julian_date() ,'lst_now' : ugradio.timing.lst()}
    #Remove first 200 samples of each data capture
    cap_list = [cap[200+16000*N:16000*(N+1)] for N in range(0, args.nblocks) ]





    #plot out a histogram of one of the blocks,
    plt.figure()
    plt.hist(cap_list[0], bins=100)
    plt.show()


    save = False
    while save == False:
        save_opt = input('Do you want to save? (y/n): ')
        if save_opt =='y':
            outfile = open(args.path+args.file_name, 'wb')
            pickle.dump(cap_list,outfile)
            outfile.close()

            outfile = open(args.path+args.file_name+'_meta_dict_initial', 'wb')
            pickle.dump(meta_dict_initial,outfile)
            outfile.close()


            outfile = open(args.path+args.file_name+'_meta_dict_final', 'wb')
            pickle.dump(meta_dict_final,outfile)
            outfile.close()
            print('done saving to: '+args.path+args.file_name)
            save =True
        elif save_opt=='n':
                return -1
        else:
            print('choose y or n')


if __name__ == '__main__':
    main()

