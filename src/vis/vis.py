#!/usr/bin/python3

import sys, getopt

import matplotlib.pyplot as plt
#import mpld3
import numpy as np
import scipy as sp
import scipy.signal as sps
import scipy.fftpack as spfft

def low_pass(cutoff, sample_rate, vector):
    try:
        b, a = sps.butter(3, cutoff/(0.5*sample_rate), 'low', analog=False)
    except ValueError:
        raise ValueError(cutoff, sample_rate, cutoff/(0.5*sample_rate))
    return sps.lfilter(b, a, vector)

def envelope(vector):
    return vector

def low_cut(vector):
    zeros = np.where(vector<=0.1)[0]
    for zero in zeros:
        try:
            vector[zero] = max(vector[zero-10:zero])
        except:
            pass
    return vector

def main(argv):

    # read data from file

    fname = argv[1]

    start = 0
    length = None
    te1, e1, te2, e2, te3, e3, te4, e4, te5, e5, te6, e6, te7, e7, te8, e8 = np.genfromtxt(fname, delimiter=' ', skip_header=start, max_rows=length, unpack=True)

    print('data read')

    # time

    t = [0]*8

    for i, vector in enumerate([te1, te2, te3, te4, te5, te6, te7, te8]):
        # fix time values that wrapped around
        t[i] = (vector - te1[0])*10**-6
        try:
            index_of = np.where(t[i]<0)[0][0]
            dt = t[i][index_of-1] - t[i][index_of]
            for j, val in enumerate(t[i][index_of:]):
                t[i][j+index_of] = val + dt
        except IndexError:
            pass
        # fix broken time values that are too high because of extra chars
        for err in np.where(t[i]>t[i][-1]):
            t[i][err] = t[i][err-1] + 0.5*(t[i][err+1] - t[i][err-1])
        # fix broken time values that are too low because of missing chars
        #TODO

    sample_rate = 1/((t[0][-1]-t[0][0])/len(t[0]))

    print('time conditioned')

    # values

    e = [0]*8
    e_raw = [0]*8
    freqs = [0]*8
    diff = [0]*8

    for i, vector in enumerate([e1, e2, e3, e4, e5, e6, e7, e8]):
        e[i] = vector / 4096
        e_raw[i] = e[i]
        #e[i] = low_pass(0.1, sample_rate, e[i])
        #e[i] = sps.savgol_filter(e[i], 99, 3)
        e[i] = envelope(e[i])
        freqs[i] = spfft.fftfreq(e_raw[i].size, t[i][1]-t[i][0])
        diff[i] = np.diff((e[i], t[i]), 2)
        #e[i] = e[i]/(max(e[i])-min(e[i]))

    print('values conditioned')

    del te1, e1, te2, e2, te3, e3, te4, e4, te5, e5, te6, e6, te7, e7, te8, e8

    # plot

    c = ['b','g','w','c','m','y','b','r']

    fig, ax = plt.subplots() #plt.subplots(nrows=2, ncols=1, sharex=True)

    fig.suptitle(fname.split('/')[-1])
    plt.style.use('bmh')

    tau = np.mean(t[0]-t[1])

    for i, (vt, ve, ve_raw, vfreq, vd) in enumerate(zip(t, e, e_raw, freqs, diff)):
        if i in [7]:

            # sal
            #plt.subplot(211)
            ax.plot(vt[2:], ve[2:], alpha=0.5, label='#'+str(i+1), color=c[i])
            ax.plot(vt[2:], ve_raw[2:], alpha=0.1, label='#'+str(i+1)+'r', color='b')#c[i])
            ax.set_xlabel('t[s]')
            ax.set_ylabel('U[V]')
            ax.legend(loc='best')

            # diff
            #plt.subplot(212)
            #ax[1].plot(vt[2:], vd[0], alpha=0.5, label='d#'+str(i+1), color=c[i])

            #print('plot', i+1, 'from 8')

            # freq
            #plt.subplot(212)
            #plt.plot(vfreq, 20*sp.log10(abs(sp.fft(ve_raw))),
            #         '.', alpha=0.6, color=c[i])

    try:
        if argv[2] == '-s':
            plt.savefig(fname.split('.')[0]+'.svg', dpi=300)
    except:
        plt.show()
        #mpld3.save_html(fig, 'plot.html')

if __name__ == "__main__":
    main(sys.argv)
