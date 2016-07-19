#!/usr/bin/python3

import sys, getopt

import matplotlib.pyplot as plt
#import mpld3
import numpy as np
import scipy as sp
import scipy.signal as sps
import scipy.fftpack as spfft

def main(argv):

    # read data from file

    fname = argv[1]

    te1, e1, te2, e2, te3, e3, te4, e4, te5, e5, te6, e6, te7, e7, te8, e8 = np.genfromtxt(fname, delimiter=' ', skip_header=100, unpack=True)

    # time

    t = [0]*8

    for i, vector in enumerate([te1, te2, te3, te4, te5, te6, te7, te8]):
        t[i] = (vector - te1[0])*10**-6
        index_of = np.where(t[i]<0)[0][0]
        dt = t[i][index_of-1] - t[i][index_of]
        for j, val in enumerate(t[i][index_of:]):
            t[i][j+index_of] = val + dt

    sample_rate = 1/((t[0][-1]-t[0][0])/len(t[0]))

    del te1, e1, te2, e2, te3, e3, te4, e4, te5, e5, te6, e6, te7, e7, te8, e8

    # plot

    c = ['b','g','w','c','m','y','b','r']

    fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True)

    fig.suptitle(fname.split('/')[-1])
    plt.style.use('bmh')

    ax.plot(t[0])

    try:
        if argv[2] == '-s':
            plt.savefig(fname.split('.')[0]+'.svg', dpi=300)
    except:
        plt.show()

if __name__ == "__main__":
    main(sys.argv)
