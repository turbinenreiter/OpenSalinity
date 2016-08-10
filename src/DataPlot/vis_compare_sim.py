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

def low_pass(cutoff, sample_rate, vector):
    try:
        b, a = sps.butter(3, cutoff/(0.5*sample_rate), 'low', analog=False)
    except ValueError:
        raise ValueError(cutoff, sample_rate, cutoff/(0.5*sample_rate))
    return sps.lfilter(b, a, vector)

def envelope(vector):
    return np.abs(sps.hilbert(vector))

def roll_max_savgol(vector):
    for i,val in enumerate(vector):
        try:
            vector[i] = max(vector[i+1:i+100])
        except:
            pass
    off = [0]*100
    global vemf
    vemf = copy.copy(vector)
    vemf = np.insert(vemf, 1, off)[:-100]
    return sps.savgol_filter(np.insert(vector, 1, off)[:-100], 333, 2)

def main(argv):

    # read data from file

    fname = argv[1]

    start = 0
    length = None
    te1, e1, te2, e2, te3, e3, te4, e4, te5, e5, te6, e6, te7, e7, te8, e8 = np.genfromtxt(fname, delimiter=' ', skip_header=start, max_rows=length, unpack=True)

    sim = np.genfromtxt('/home/plam/Documents/Semesterarbeit/OpenSalinity/src/sim_comp/data/1.6/simulationData.csv', names=True, delimiter=';', skip_header=4)

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
    means = [0]*8

    for i, vector in enumerate([e1, e2, e3, e4, e5, e6, e7, e8]):
        e[i] = vector / 4096
        means[i] = np.mean(e[i][3000:4000])
        e[i] = e[i] * (means[0]/means[i])
        e_raw[i] = copy.copy(e[i])
        #e[i] = low_pass(0.1, sample_rate, e[i])
        #e[i] = sps.savgol_filter(e[i], 99, 3)
        e[i] = roll_max_savgol(e[i])
        #e[i] = envelope(e[i])
        freqs[i] = spfft.fftfreq(e_raw[i].size, t[i][1]-t[i][0])
        diff[i] = np.diff((e[i], t[i]), 2)
        #e[i] = e[i]/(max(e[i])-min(e[i]))

    print('values conditioned')

    del te1, e1, te2, e2, te3, e3, te4, e4, te5, e5, te6, e6, te7, e7, te8, e8

    # plot

    #     0   1   2   3   4   5   6   7
    c = ['b','y','k','c','m','g','g','r']

    fig, axg = plt.subplots() #plt.subplots(nrows=2, ncols=1, sharex=True)

    #fig.suptitle(fname.split('/')[-1])
    #plt.style.use('bmh')

    tau = np.mean(t[0]-t[1])

    grid = gs.GridSpec(3,2)
    sp = [0]*8
    count = 0

    for i, (vt, ve, ve_raw, vfreq, vd) in enumerate(zip(t, e, e_raw, freqs, diff)):
        if i in [0,1,3,4,5,7]: #0,1,2,3,4,5,6,7

            sp[count] = fig.add_subplot(grid[count])
            ax = sp[count]
            count = count + 1

            s = 10000
            e = -28000
            # sal
            #plt.subplot(211)
            ax.plot(vt[s:e], ve[s:e], alpha=0.75, label='#'+str(i+1),
                    color=c[i], linewidth=1.5)
            #ax.plot(vt[s:e], vemf[s:e], alpha=0.50, label='#'+str(i+1), color='b', linewidth=1.5)
            #ax.scatter(vt[s:e], ve_raw[s:e], alpha=0.25,
            #           label='#'+str(i+1)+'raw', color=c[i], marker='.')

            dt = +66.5+2.5
            sc = max(ve)
            ax.scatter(sim['Time']+dt, sim['Sensor_'+str(i+1)]*sc,
                       alpha=0.25, color=c[i], marker='.')

            ax.set_yticks([0.0,0.3,0.6,0.9])

            if count%2 == 0:
                ax.set_yticklabels([])
            if count < 6-2:
                ax.set_xticklabels([])

            ax.set_ylim([0,1])
            ax.set_xlim([vt[s],vt[e]])
            ax.grid(True, linestyle='dashed')

            lfont = {'fontname':'Source Serif Pro'}
            axg.set_xlabel('Time, s', **lfont, labelpad=24)
            axg.set_ylabel('relative Voltage, -', **lfont, labelpad=32)
            axg.set_yticks([])
            axg.set_xticks([])
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
