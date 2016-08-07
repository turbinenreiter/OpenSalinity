#!/usr/bin/python3

import sys, getopt

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sps

def main(argv):

    # read data from file

    fname = argv[1]

    millis, e1 = np.genfromtxt(fname, delimiter=',', unpack=True)

    # time

    t = [0]*1

    millis = millis - millis[0]

    dt = np.append(np.ediff1d(millis)/8, 0)

    for i in range(1):
        t[i] = (millis + i*dt/8) / 1000

    # values

    e = [0]*1

    for i, vector in enumerate([e1]):
        e[i] = vector / 4096
        #e[i] = sps.savgol_filter(e[i], 99, 3)
        #e[i] = e[i]/(max(e[i])-min(e[i]))

    del millis, e1

    # plot

    #plt.title('')
    #plt.style.use('bmh')

#    for i, (vt, ve) in enumerate(zip(t, e)):
#        if i < 4: c = 'b'
#        else: c = 'r'
#        plt.plot(vt, ve, color=c, alpha=0.6)

    plt.scatter(t[0], e[0], color='b', alpha=0.5, marker='.')
    #plt.plot(t[0], e[0], color='b', alpha=0.5)

    plt.arrow(t[0][999], 1, 0, -0.2, color='red', alpha=0.5)

    plt.axvline(x=t[0][999], linewidth=1, color='r', alpha=0.25)
    #ln2(10K*1uF)=0.0069s - Halbwertszeit Kondensator
    if fname.split('.')[0][-1] == '1':
        #plt.plot(t[0][1020], e[0][1020], 'o', color='r', alpha=0.25)
        plt.axvline(x=t[0][1130], linewidth=1, color='r', alpha=0.25)
        plt.text(t[0][1200],0.2, str(t[0][1130]-t[0][999])+'s')

    plt.xlabel('Time, s')
    plt.ylabel('Voltage, V')

    plt.ylim([0,1])

    try:
        if argv[2] == '-s':
            plt.savefig(fname.split('.')[0]+'.svg', dpi=300, facecolor='white', edgecolor='none')
            from matplotlib2tikz import save as tikz_save
            tikz_save(fname.split('.')[0]+'.tex')
    except:
        plt.show()

if __name__ == "__main__":
    main(sys.argv)
