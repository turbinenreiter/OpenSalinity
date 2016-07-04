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

    plt.title(fname.split('/')[-1])
    plt.style.use('bmh')

#    for i, (vt, ve) in enumerate(zip(t, e)):
#        if i < 4: c = 'b'
#        else: c = 'r'
#        plt.plot(vt, ve, color=c, alpha=0.6)

    plt.plot(e[0], color='b', alpha=0.6)

    plt.axvline(x=t[0][999], linewidth=1, color='r')
    #ln2(10K*1uF)=0.0069s - Halbwertszeit Kondensator
    #plt.plot(t[0][1020], e[0][1020], 'o', color='r', alpha=0.6)
    #plt.axvline(x=t[0][1130], linewidth=1, color='r')
    #plt.text(t[0][1200],0.2, str(t[0][1130]-t[0][999])+'s')

    plt.xlabel('t[s]')
    plt.ylabel('U[V]')

    try:
        if argv[2] == '-s':
            plt.savefig(fname.split('.')[0]+'.svg', dpi=300)
    except:
        plt.show()

if __name__ == "__main__":
    main(sys.argv)
