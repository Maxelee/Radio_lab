from numpy.fft import fft, fftshift, fftfreq
import matplotlib.pyplot as plt
from numpy import abs, median, diff, linspace

def get_power(data_real, data_imaginary=None):
    if data_imaginary is None:
        data = data_real
    else:
        data = data_real + 1.0j*data_imaginary
    return abs(fft(data))**2

def get_times_and_freqs(N, v_sample):
    times = linspace(0, N/v_sample, N)
    freqs = fftfreq(len(times), median(diff(times)))
    return times, freqs

def plot_power(file_name, N, v_sample, data_real, data_imaginary=None):
    power = get_power(data_real, data_imaginary)
    times, freqs = get_times_and_freqs(N, v_sample)
    plt.figure()
    plt.plot(fftshift(freqs/1e6), fftshift(power))
    plt.savefig(file_name+'.pdf')


