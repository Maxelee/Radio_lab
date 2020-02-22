import numpy as np
import glob
import pickle

path = '/home/maxlee1993/Documents/radio_lab/Radio_lab/Lab_2/data/captures/2458901/'

files_on_1 = path + 'cap_5-74_s_on_1231'
files_on_2 = path + 'cap_5-77_s_on_part2'
files_off_1 = path + 'cap_5-68_s_off_1229'
files_off_2 = path + 'cap_5-71_s_off_part2'

infile = open(files_on_1, 'rb')
son = pickle.load(infile)
infile.close()
infile = open(files_on_2, 'rb')
son_2 = pickle.load(infile)
infile.close()
infile = open(files_off_1, 'rb')
soff = pickle.load(infile)
infile.close()
infile = open(files_off_2, 'rb')
soff_2 = pickle.load(infile)
infile.close()
print('done importing s_on')

s_on =np.asarray( son['real']+son_2['real']) +1.0j*np.asarray( son['imaginary']+son_2['imaginary'])

s_off = np.asarray(soff['real']+soff_2['real']) + 1.0j*np.asarray(soff['imaginary']+soff_2['imaginary'])

print(s_on.shape)

s_on_power = np.mean(np.abs(np.fft.fft(s_on, axis=1))**2, axis=0)
s_off_power = np.mean(np.abs(np.fft.fft(s_off, axis=1))**2, axis=0)
print('done power for s')
files_on_1 = path + 'cap_5-86_galaxy_on'
files_on_2 = path + 'cap_5-89_galaxy_on_take2'
files_off_1 = path + 'cap_5-92_galaxy_off'
files_off_2 = path + 'cap_5-95_galaxy_off_take2'
print('imported files for galaxy')
infile = open(files_on_1, 'rb')
galaxyon = pickle.load(infile)
infile.close()
infile = open(files_on_2, 'rb')
galaxyon_2 = pickle.load(infile)
infile.close()
infile = open(files_off_1, 'rb')
galaxyoff = pickle.load(infile)
infile.close()
infile = open(files_off_2, 'rb')
galaxyoff_2 = pickle.load(infile)
infile.close()

s_on =np.asarray( galaxyon['real']+galaxyon_2['real']) +1.0j*np.asarray( galaxyon['imaginary']+galaxyon_2['imaginary'])

s_off = np.asarray(galaxyoff['real']+galaxyoff_2['real']) + 1.0j*np.asarray(galaxyoff['imaginary']+galaxyoff_2['imaginary'])


galaxy_on_power = np.mean(np.abs(np.fft.fft(s_on, axis=1))**2, axis=0)
galaxy_off_power = np.mean(np.abs(np.fft.fft(s_off, axis=1))**2, axis=0)


print('done power for galaxy')
outfile = open(path+'galaxy_on_power', 'wb')
pickle.dump(galaxy_on_power, outfile)
outfile.close()
outfile = open(path+'galaxy_off_power', 'wb')
pickle.dump(galaxy_off_power, outfile)
outfile.close()
outfile = open(path+'s_on_power', 'wb')
pickle.dump(s_on_power, outfile)
outfile.close()
outfile = open(path+'s_off_power', 'wb')
pickle.dump(s_off_power, outfile)
outfile.close()

print('done pickling')
