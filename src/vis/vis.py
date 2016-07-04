#!/usr/bin/python3

import sys, getopt

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sps

def main(argv):

    # read data from file

    fname = argv[1]

    te1, e1, te2, e2, te3, e3, te4, e4, te5, e5, te6, e6, te7, e7, te8, e8 = np.genfromtxt(fname, delimiter=' ', unpack=True)

    # time

    t = [0]*8

    for i, vector in enumerate([te1, te2, te3, te4, te5, te6, te7, te8]):
        t[i] = vector - te1[0]

    # values

    e = [0]*8

    for i, vector in enumerate([e1, e2, e3, e4, e5, e6, e7, e8]):
        e[i] = (vector - np.average(vector[0:100])) / 4096
        e[i] = sps.savgol_filter(e[i], 99, 3)
        #e[i] = e[i]/(max(e[i])-min(e[i]))

    del te1, e1, te2, e2, te3, e3, te4, e4, te5, e5, te6, e6, te7, e7, te8, e8

    # plot

    plt.title(fname.split('/')[-1])
    plt.style.use('bmh')

    for i, (vt, ve) in enumerate(zip(t, e)):
#        if i < 2: c = 'b'
#        else: c = 'r'
        if i < 4:
            plt.plot(vt, ve, alpha=0.6, label='line'+str(i))

    plt.xlabel('t[s]')
    plt.ylabel('U[V]')

    plt.legend(loc='best')

    try:
        if argv[2] == '-s':
            plt.savefig(fname.split('.')[0]+'.svg', dpi=300)
    except:
        plt.show()

if __name__ == "__main__":
    main(sys.argv)
