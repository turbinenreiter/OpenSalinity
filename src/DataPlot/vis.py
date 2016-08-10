#!/usr/bin/python3

import sys, getopt

import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import copy
#import mpld3
import numpy as np
import scipy as sp
import scipy.signal as sps
import scipy.fftpack as spfft
from math import ceil

def low_pass(cutoff, sample_rate, vector):
    try:
        b, a = sps.butter(3, cutoff/(0.5*sample_rate), 'low', analog=False)
    except ValueError:
        raise ValueError(cutoff, sample_rate, cutoff/(0.5*sample_rate))
    return sps.lfilter(b, a, vector)

def envelope(vector):
    return np.abs(sps.hilbert(vector))

e_rm = []
def roll_max_savgol(vector):
    for i,val in enumerate(vector):
        try:
            vector[i] = max(vector[i+1:i+100])
        except:
            pass
    vrm = copy.copy(vector)
    e_rm.append(vrm)
    #vemf = np.insert(vemf, 1, [0]*100)[:-100]
    return sps.savgol_filter(vrm, 333, 2)

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

    print('time conditioned')

    # values
    e = [0]*8
    e_raw = [0]*8
    freqs = [0]*8
    diff = [0]*8
    means = [0]*8

    for i, vector in enumerate([e1, e2, e3, e4, e5, e6, e7, e8]):
        e[i] = vector / 4096
        means[i] = np.mean(e[i][3000:4000])
        e[i] = e[i] * (means[0]/means[i])
        e_raw[i] = copy.copy(e[i])
        e[i] = roll_max_savgol(e[i])
        freqs[i] = spfft.fftfreq(e_raw[i].size, t[i][1]-t[i][0])
        diff[i] = np.diff((e[i], t[i]), 2)

    print('values conditioned')

    del te1, e1, te2, e2, te3, e3, te4, e4, te5, e5, te6, e6, te7, e7, te8, e8

    # plot

    #     0   1   2   3   4   5   6   7
    c = ['b','y','k','c','m','g','g','r']

    fig, axg = plt.subplots()

    maxve = 0

    for i, (vt, ve, ve_raw, vfreq, vd, vrm) in enumerate(zip(t, e, e_raw, freqs, diff, e_rm)):
        if i in [3,7]: #0,1,2,3,4,5,6,7

            ax = axg

            ts = 25
            te = 225

            s = np.where(vt>=ts)[0][0]
            e = np.where(vt>=te)[0][0]

            # sal

            dt = vt[s+100]-vt[s]

            ax.plot(vt[s:e]+dt, ve[s:e], alpha=0.75, label='#'+str(i+1),
                    color=c[i], linewidth=1.75)

            #ax.plot(vt[s:e]+dt, vrm[s:e], alpha=0.50,
            #        label='#'+str(i+1), color=c[i], linewidth=1.5)

            #ax.scatter(vt[s:e], ve_raw[s:e], alpha=0.25,
            #           label='#'+str(i+1)+'raw', color=c[i], marker='.')

            if max(ve[s:e]) > maxve:
                maxve = max(ve[s:e])
                ax.set_ylim([0,ceil(max(ve[s:e])*10)/10])
            ax.set_xlim([vt[s],vt[e]])
            ax.grid(True, linestyle='dashed')

            lfont = {'fontname':'Source Serif Pro'}
            axg.set_xlabel('Time, s', **lfont)#, labelpad=24)
            axg.set_ylabel('relative Voltage, -')#, **lfont, labelpad=32)
            #axg.set_yticks([])
            #axg.set_xticks([])
            #axg.xaxis.set_visible(False)
            #axg.yaxis.set_visible(False)

            # diff
            #plt.subplot(212)
            #ax[1].plot(vt[2:], vd[0], alpha=0.5, label='d#'+str(i+1), color=c[i])

            #print('plot', i+1, 'from 8')

            # freq
            #plt.subplot(212)
            #plt.plot(vfreq, 20*sp.log10(abs(sp.fft(ve_raw))),
            #         '.', alpha=0.6, color=c[i])

    fig.tight_layout()

    try:
        if argv[2] == '-s':
            plt.savefig(fname.split('.')[0]+'.pdf', dpi=300)
            from matplotlib2tikz import save as tikz_save
            tikz_save(fname.split('.')[0]+'.tex')
    except:
#    else:
        plt.show()
        #mpld3.save_html(fig, 'plot.html')

if __name__ == "__main__":
    main(sys.argv)
