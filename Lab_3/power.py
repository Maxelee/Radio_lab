import numpy as np

def get_power(data):
    return np.abs(np.fft.fft(data))**2
def read_file(path, file_name):
    data = np.load(path+file_name, allow_pickle=True)
    return data
def write_file(path, file_name, data):
    np.savez(path+file_name, data)

