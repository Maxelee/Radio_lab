import numpy as np

def get_real_file(l, b=0.0):
    try:
        _,b = str(b).split('-')
        b = 'n'+str(b)
    except:
        pass
    file = f'divided_2/{l}_{b}_line.npz'
    f_in = np.load(file, allow_pickle=True)
    f_in = f_in['real0']*1000
    f_in  = np.nan_to_num(f_in, 0)
    f_in  -= np.mean(f_in)
    f_in[:2500] = 0
    f_in[5200:] = 0
    return f_in

def main():
    xs = np.arange(-50, 50, .1)
    ys = np.arange(-50, 50, .1)
    zs = np.arange(-5, 5, .1)
    f = np.linspace(145e6, 155e6, 8192)+1270e6
    v = 3e8*(1420.4e6 - f)/1420.4e6/1e3-13
    sun_pos = np.array([0, -8, 0])
    sun_v = np.array([-220, 0, 0])
    sun_mag = np.linalg.norm(sun_pos)
    grid = np.array([(y, x, z) for x in xs for y in ys for z in zs])
    print('grid made')
    delta_x = (grid-sun_pos).T/np.linalg.norm(grid-sun_pos, axis=1)
    phi = np.arctan2(grid[:,1], grid[:,0])
    delta_v = 220*np.array([np.sin(phi), np.cos(phi), np.zeros_like(phi)]).T - sun_v

    doppler_grid = np.einsum('ij, ji->i',delta_v, delta_x).reshape(xs.size, ys.size, zs.size)


    power_grid = np.zeros((len(xs), len(ys),len(zs), 1))
    file_count = []
    file_errors = 0
    index_errors = 0
    # Loop over x values and y values
    print('starting to make power grid... here we goooooo')
    for j,x in enumerate(xs[:]):
        for i,y in enumerate(ys[:]):
            for k, z in enumerate(zs):

                l_init = (90-np.arctan2(y-sun_pos[1],x-sun_pos[0])*180/np.pi)%360
                L= np.round(l_init/2)*2

                b_init = np.arctan2(z, np.linalg.norm([x,y]))*180/np.pi
                B = np.round(b_init/2)*2
                try:
                    file = get_real_file(L, B)

                    if not [L, B] in file_count:
                        file_count.append([L, B])

                except FileNotFoundError:
                    file_errors+=1
                    pass

                # find the doppler velocity at that point
                doppler_v = doppler_grid[i,j, k]
                # find the point in the spectra/spectras that has that velocity
                assert v[0]>doppler_v>v[-1] # Doppler velocity outside bounds
                v_index = np.where(doppler_v<v)[0][-1]+1

                # assign that point its corresponding power
                power = file[v_index]
                power_grid[i,j, k] += power


        if j%50==0:
            print(f'x={j}/{len(xs)} done, file errors: {file_errors}')
            file_errors =0
            index_errors = 0
    np.savez('power_grid.npz', power_grid)

if __name__ == '__main__':
    main()
