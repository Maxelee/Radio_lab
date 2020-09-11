from ugradio.pico import capture_data as cpd
import numpy as np
import argparse
from utils import get_pos, get_times,save
import time
parser = argparse.ArgumentParser(description='Capture bighirn data.')

parser.add_argument('--volt_range',metavar='volt_range', type=str, default='1V',help='volt range of pico sampler')
parser.add_argument('--divisor', metavar='divisor', type=int,default=1, help='divisor for the sampling frequency')
parser.add_argument('--path',metavar='path', type=str, default='/home/maxlee1993/Documents/radio_lab/Radio_lab/Lab_2/data/',help=' directory to save the data')
parser.add_argument('--file_name',metavar='file_name', type=str, default='cap',help=' directory to save the data')
parser.add_argument('--nblocks',metavar='nblocks', type=int, default=1, help='number of blocks to use')
parser.add_argument('--ra', metavar='ra', type=str, default=None, help='right ascension string in h:m:s')
parser.add_argument('--dec', metavar='dec', type=str, default=None, help='declination string in d:m:s')
parser.add_argument('--alt', metavar='alt', type=float, default=None, help='altitude in degrees')
parser.add_argument('--az', metavar='az', type=float, default=None, help='azimuth in degrees')
parser.add_argument('--lat', metavar='lat', type=float, default=None, help='latitude in degrees')
parser.add_argument('--long', metavar='long', type=float, default=None, help='longitude in degrees')
parser.add_argument('--lat_loc', metavar='lat_loc', type=float, default=37.873199, help='latitude in degrees of observation')
parser.add_argument('--iterations', metavar='iterations', type=int, default=None, help='whether to iterate over multiple captures')
args=parser.parse_args()

def main():

    t0 = get_times()
    #Capture the data
    if args.iterations is None:
        cap = cpd(nsamples=100000, divisor=args.divisor, volt_range=args.volt_range, nblocks=args.nblocks, dual_mode=True)
        print(cap.shape)
    else:
        cap=[]
        for i in range(args.iterations):
            cap.append(cpd(divisor=args.divisor, volt_range=args.volt_range, nblocks=args.nblocks, dual_mode=True))
            print('completed {} captures'.format(i+1))

    tf = get_times()

    cap = np.array(cap).reshape(args.iterations, 2, -1, 100000)
    cap = cap.transpose([1,0,2,3]).copy()
    cap.shape = (2, -1, 100000)
    #Organize real and complex components
    #cap = organize_caps(cap, args)

    #test with a histogram
    #test_hist(cap)


    # Compute coordintes before and after data capture, store in dict
    coords_0 = get_pos(args, t0)
    coords_f = get_pos(args, tf)
    np.savez(args.path + '\captures' + args.file_name , real=cap[0], image=cap[1], t0=t0, tf=tf, coords_0=coords_0, coords_f=coords_f)
    #Save data
    #save(args, cap, t0, tf)


if __name__ == '__main__':
    main()

