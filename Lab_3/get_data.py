from ugradio import hp_multi, timing, interf
import os
import argparse
from time import sleep
import numpy as np
my_parser = argparse.ArgumentParser(prog='get_data', description='Capture inter data')

# Add the arguments
my_parser.add_argument('--sleep_time', metavar='--sleep_time', type=int,help='how long before clearing buffer', default=1800)
my_parser.add_argument('--dt', metavar='--dt',type=float, help='integration time length in seconds', default=1)
my_parser.add_argument('--path', metavar='--path', type=str, help='path to save to', default='/home/maxlee1993/Documents/radio_lab/Radio_lab/Lab_3/data/interf_data')
my_parser.add_argument('--threshold', metavar='--threshold', type=int, default=3, help='number of iterations')
args = my_parser.parse_args()

def main():
    ################ ORGANIZING FILES AND DIRECTORIES #############
    # Check if the JD exists
    JD = timing.julian_date()
    path = args.path + '/' + str(round(int(JD)))
    path_exists = os.path.exists(path)
    if path_exists:
        pass
    else:
        os.mkdir(path)

    hpm = hp_multi.HP_Multimeter()
    ifm = interf.Interferometer()
    t0  = []
    hpm.start_recording(args.dt)
    try:
        for j in range(args.threshold):

            # Create file_name
            file_name = 'capture'+str(j)

            #Write the time it starts taking data
            t0.append(timing.lst())
            #store data in the buffer
            print(t0)
            # print recording progress
            print(hpm.get_recording_status())
            print('j = {}, time={}'.format(j, timing.lst()))
            # Wait an hour
            for i in range(int(args.sleep_time/60)):
                sleep(60)
                print('sleeping for {} min'.format(i))

            #clear buffer and save every hour
            data, times = hpm.get_recording_data()
            print('made data and times')
            np.savez(path+'/'+file_name, voltage_data=np.array(data), times=np.array(times), t0=np.array(t0))
            print('saved at j={}'.format(j))
    except KeyboardInterrupt:
        data, times = hpm.get_recording_data()
        np.savez(path+'/'+file_name, voltage_data=np.array(data), times=np.array(times), t0=np.array(t0))
        hpm.end_recording()
    finally:
        data, times = hpm.get_recording_data()
        np.savez(path+'/'+file_name, voltage_data=np.array(data), times=np.array(times), t0=np.array(t0))
        hpm.end_recording()
    hpm.end_recording()
    return 0
if __name__=='__main__':
    main()
