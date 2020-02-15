from ugradio import pico as ugp
from numpy import savez, median, diff
from numpy.fft import fftfreq, fftshift, fft
import argparse
import matplotlib.pyplot as plt
parser =argparse.ArgumentParser(description='')
parser.add_argument("--file_name", required=True, help='File name to save')
parser.add_argument("--path", default='/home/maxlee1993/Documents/', help='Path to file')
parser.add_argument("--volt_range", default='1V', help='Voltrange for Pico')
parser.add_argument("--divisor", default=1, help='divisor for sample freq')
parser.add_argument("--nblocks", default=1, help='blocks to take')
parser.add_argument("--dual_mode", default=False, help='take both channels')

args = parser.parse_args()

filepath = args.path+args.file_name
wf = ugp.capture_data(divisor=int(args.divisor), volt_range=args.volt_range, nblocks=int(args.nblocks), dual_mode=args.dual_mode)
savez(filepath, wf)

times = np.linspace(0, len(wf)/((62.5/args.divisor)*1e6), len(wf))
freqs = fftfreq(len(times), median(diff(times)))

power = abs(fft(wf))**2

plt.figure()
plt.plot(shift(freqs/1e6), shift(power))
plt.show()
