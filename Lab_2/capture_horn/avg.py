import numpy as np


load_on = np.load('/home/maxlee1993/Documents/radio_lab/Radio_lab/Lab_2/data/captures/cas_on4.npz')
load_off = np.load('/home/maxlee1993/Documents/radio_lab/Radio_lab/Lab_2/data/captures/cas_off4.npz')
print('loaded data')
real_on = load_on['real']
real_off = load_off['real']

image_on= load_on['image']
image_off=load_off['image']

single_on = (np.abs(np.fft.fft(real_on+1.0j*image_on, axis=1))**2)[0]
single_off = (np.abs(np.fft.fft(real_off+1.0j*image_off, axis=1))**2)[0]

mean_on = np.mean(np.abs(np.fft.fft(real_on+1.0j*image_on, axis=1))**2, axis=0)

mean_off = np.mean(np.abs(np.fft.fft(real_off+1.0j*image_off, axis=1))**2, axis=0)
print('averaged power')
median_on = np.median(np.abs(np.fft.fft(real_on+1.0j*image_on, axis=1))**2, axis=0)

median_off = np.median(np.abs(np.fft.fft(real_off+1.0j*image_off, axis=1))**2, axis=0)
np.savez('/home/maxlee1993/Documents/radio_lab/Radio_lab/Lab_2/data/captures/power_cas_on4.npz', avg=mean_on, median=median_on, single =single_on)
np.savez('/home/maxlee1993/Documents/radio_lab/Radio_lab/Lab_2/data/captures/power_cas_off4.npz', avg=mean_off, median=median_off, single =single_off)
print('done saving')
