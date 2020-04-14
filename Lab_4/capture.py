import numpy as np
import sys
import os


import argparse
from utils import get_pos, get_times
import time
parser = argparse.ArgumentParser(description='generate observing grid.')
parser.add_argument('--ls', nargs='+', type=float, required=True, help='galactic latitude min and max in degrees')
parser.add_argument('--bs', nargs='+', type=float, required=True, help='Galactic longitude min and max in degrees')
parser.add_argument('--l_resolution', type=int, required=True, help='Latitude resolution in degrees')
parser.add_argument('--b_resolution', type=int, required=True, help='Longitude resolution in degrees')
parser.add_argument('--time', metavar='--time',type=int, help='desired total observation time at each coord', default=1)
parser.add_argument('--path', metavar='--path', type=str, help='path to save to', default='/home/radiolab/boyx')
parser.add_argument('--noise', metavar='--noise',type=str, help='noise on or off', default='off')
parser.add_argument('--LO', metavar='--LO',type=float, help='set the desired LO frequency (do not need to worry about frequency doubling, that will be taken into consideration)', default= 635)
parser.add_argument('--LO_unit', metavar='--LO_unit', type=str, help='LO frequency units',default='MHz')
parser.add_argument('--power',metavar='--power',type=float,help='LO power',default=10.0)
parser.add_argument('--power_unit',metavar='--power_unit',type=str,help='LO power units',default='dBm')
args=parser.parse_args()

def start_generator(grid, start_l, start_b):
    for idx_l in range(grid.shape[0]):
        for idx_b in range(grid.shape[1]):
            yield  grid[(idx_l + start_l) % grid.shape[0], (idx_b+start_b)%grid.shape[1], :]


def make_grid(args):

    g_ls = np.arange(args['ls'][0], args['ls'][1]+1, args['l_resolution'])
    g_bs = np.arange(args['bs'][0], args['bs'][1]+1, args['b_resolution'])

    grid = np.zeros((len(g_ls), len(b_ls), 2))
    ls = np.arange(0, 360+1, 2)

    counter = 0
    for i, l in enumerate(ls):
        for j,b in enumerate(bs):
            if counter%4 !=0:
                b = -b
            grid_lb[i, j] = l,b                                                  # Store the l and bs in thier own array for easy viewing
            c = SkyCoord(l, b, frame='galactic',unit='deg')
            ra_dec = c.transform_to('fk5')                                       # convert the l,b to ra, dec and store in grid
            grid[i,j,0]  = ra_dec.ra.radian
            grid[i, j, 1] = ra_dec.dec.radianreturn altaz.alt.deg, altaz.az.deg
    g = start_generator(grid, int(116), 0)
    g_lb = start_generator(grid_lb, int(116), 0)
    pointings = np.array([coord for coord in g])
    pointings_lb = np.array([coord for coord in g_lb])
    return pointings, pointings_lb

def point():
    JD = timing.julian_date()
    spec = leusch.Spectrometer()
    noise = leusch.LeuschNoise()
    lo = agilent.SynthDirect()
    telescope = leusch.LeuschTelescope()
    grid, grid_lb= get_grid(args)
    if args.noise=='on':
        noise.on()
        path_ending = 'noise_on.fits'
    else:
        noise.off()
        path_ending = '.fits'


    print(spec.check_connected()) # checks for proper connection
    int_time = spec.int_time() #default spectrometer int_time per spectra
    nspec = int(args.time/int_time) #calculate number of spectra captures we need in order to get desired total integration time
    lo.set_amplitude(args.power,args.power_unit) #set LO power
    lo.set_frequency(args.LO/2,args.LO_unit) #set LO frequency

    for j, coord in enumerate(pointings):
        path = args.path+f'/{args.LO}_{grid_lb[j][0]}_{grid_lb[j][1]}_' +path_ending
        alt, az = coord.get_altaz(coord[0], coord[1])
        if alt >85  or if alt <15 or if az%(360) < 5 or if az%(360) >350:
            pass
        elif os.path.exists(path):
            pass
        else:
            telescope.point(alt, az)
            tru_alt, tru_alt = telescope.get_pointing()
            print(f'Recording: {args.nspec} at {tru_alt}, {tru_az} for {int_time}, seconds')
            spec.read_spec(path, args.nspec, coord,'eq')

if __name__=='__main__':
    main()
