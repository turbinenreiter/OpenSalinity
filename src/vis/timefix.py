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

    te1, e1, te2, e2, te3, e3, te4, e4, te5, e5, te6, e6, te7, e7, te8, e8 = np.genfromtxt(fname, delimiter=' ', unpack=True)

    # time

    t = [0]*8
    dt = [0]*8

    for i, vector in enumerate([te1, te2, te3, te4, te5, te6, te7, te8]):
        t[i] = (vector - te1[0] + 270942889)
        try:
            index_of = np.where(t[i]<0)[0][0]
            dt = t[i][index_of-1] - t[i][index_of]
            for j, val in enumerate(t[i][index_of:]):
                t[i][j+index_of] = val + dt
        except IndexError:
            pass
        dt[i] = np.diff(t[i])
        i_err = (np.where(dt[i]<0))
        for err in i_err:
            try:
                print(err)
                t[i][err] = t[i][err-1]+0.5(t[i][err+1]-t[i][err-1])
            except TypeError:
                pass

    te1, te2, te3, te4, te5, te6, te7, te8 = t
    data = [te1, e1, te2, e2, te3, e3, te4, e4, te5, e5, te6, e6, te7, e7, te8, e8]
    np.savetxt(fname[:-4]+'shifted.csv', data, delimiter=0)

    sample_rate = 1/((t[0][-1]-t[0][0])/len(t[0]))

    del te1, e1, te2, e2, te3, e3, te4, e4, te5, e5, te6, e6, te7, e7, te8, e8

    # plot

    c = ['b','g','w','c','m','y','b','r']

    fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True)

    fig.suptitle(fname.split('/')[-1])
    plt.style.use('bmh')

    for i in [0,1,2,3,4,5,6,7]:
        ax.plot(t[i])

    try:
        if argv[2] == '-s':
            plt.savefig(fname.split('.')[0]+'.svg', dpi=300)
    except:
        plt.show()

if __name__ == "__main__":
    main(sys.argv)
