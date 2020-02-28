import numpy as np
import pickle

path = '/home/maxlee1993/Documents/radio_lab/Radio_lab/Lab_2/data/captures/2458902/'
infile = open('/home/maxlee1993/Desktop/'+ 'cap_5-73_s_off' , 'rb')
lower_sb = pickle.load(infile)
infile.close()


infile = open('/home/maxlee1993/Desktop/'+ 'cap_5-79_s_on' , 'rb')
upper_sb = pickle.load(infile)
infile.close()

print('imported files')


real_on = np.asarray(upper_sb['real'])
real_off = np.asarray(lower_sb['real'])
imaginary_on = np.asarray(upper_sb['imaginary'])
imaginary_off = np.asarray(lower_sb['imaginary'])
print(real_on.shape)

power_on = np.median(np.abs(np.fft.fft(real_on+1.0j*imaginary_on, axis=1))**2, axis=0)
power_off = np.median(np.abs(np.fft.fft(real_off+1.0j*imaginary_off, axis=1))**2, axis=0)

print('Made Power')
outfile = open(path +'power_on_1230', 'wb')
pickle.dump( power_on, outfile)
outfile.close()


outfile = open(path +'power_off_1225', 'wb')
pickle.dump(power_off, outfile)
outfile.close()

print('Done exporting Files')

