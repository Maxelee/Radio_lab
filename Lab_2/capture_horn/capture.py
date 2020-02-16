from ugradio.pico import capture_data as cpd
import numpy as np
import argparse
from utils import *

parser = argparse.ArgumentParser(description='Capture bighirn data.')

parser.add_argument('--volt_range',metavar='volt_range', type=str, default='1V',help='volt range of pico sampler')
parser.add_argument('--divisor', metavar='divisor', type=int,default=1, help='divisor for the sampling frequency')
parser.add_argument('--path',metavar='path', type=str, default='/home/maxlee1993/Documents/radio_lab/Radio_lab/Lab_2/data/',help=' directory to save the data')
parser.add_argument('--nblocks',metavar='nblocks', type=int, default=1, help='number of blocks to use')
parser.add_argument('--ra', metavar='ra', type=str, default=None, help='right ascension string in h:m:s')
parser.add_argument('--dec', metavar='dec', type=str, default=None, help='declination string in d:m:s')
parser.add_argument('--alt', metavar='alt', type=float, default=None, help='altitude in degrees')
parser.add_argument('--az', metavar='az', type=float, default=None, help='azimuth in degrees')
parser.add_argument('--lat', metavar='lat', type=float, default=None, help='latitude in degrees')
parser.add_argument('--long', metavar='long', type=float, default=None, help='longitude in degrees')
args=parser.parse_args()

def main():

    t0 = get_times()
    #Capture the data
    cap = cpd(divisor=args.divisor, volt_range=args.volt_range, nblocks=args.nblocks, dual_mode=True)
    tf = get_times()

    #Organize real and complex components
    cap = organize_caps(cap, args)

    #test with a histogram
    test_hist(cap)

    #Save data
    save(args, cap, t0, tf)
if __name__ == '__main__':
    main()

