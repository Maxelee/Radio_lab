import numpy as np


def power_mean(args, data):
    mean = np.mean(np.abs(np.fft.fft(data, axis=1))**2, axis=0)

def get_power(data_real, data_image=None):
    if data_image is not None:
        data = data_real+ 1.0j*data_image
    else:
        data = data_real
    return np.abs(np.fft.fft(data)**2)



