import numpy as np
import ugradio.pico as ugp
import os
import glob

wf = ugp.capture_data(divisor=2, volt_range='2V')
np.savez('/home/maxlee1993/Documents/Lab_1_freq_res/', wf)
print('saved')
print(sorted(glob.glob('/home/maxlee1993/Documents/Lab_1_freq_res/'+'*')))
