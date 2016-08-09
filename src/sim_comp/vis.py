#!/usr/bin/python3

import sys, getopt

import matplotlib.pyplot as plt
import copy
import numpy as np
import scipy as sp
import scipy.signal as sps
import scipy.fftpack as spfft


def main(argv):

    # read data from files

    env = np.genfromtxt('/home/plam/Documents/Semesterarbeit/OpenSalinity/src/sim_comp/data/1.6/log080716_2_envelope.csv', names=True, delimiter=';', skip_header=4)
    raw = np.genfromtxt('/home/plam/Documents/Semesterarbeit/OpenSalinity/src/sim_comp/data/1.6/log080716_2_rawData.csv', names=True, delimiter=';', skip_header=4)
    sim = np.genfromtxt('/home/plam/Documents/Semesterarbeit/OpenSalinity/src/sim_comp/data/1.6/simulationData.csv', names=True, delimiter=';', skip_header=4)

    data = {'env':env, 'raw':raw,'sim':sim}

    print('data read')

    # plot

    #     0   1   2   3   4   5   6   7
    c = ['b','b','b','b','g','g','g','r']

    fig, ax = plt.subplots()

    s = 0
    e = 0


    dt = -0

    for i in [4,8]:

        ax.scatter(data['sim']['Time']+dt, data['sim']['Sensor_'+str(i)],
                alpha=0.75, color=c[i-1])

        ax.plot(data['env']['Time'], data['env']['Sensor_'+str(i)],
                alpha=0.75, color=c[i-1], linewidth=1.5)
        #ax.scatter(data['raw']['Time'], data['raw']['Sensor_'+str(i)],
        #           alpha=0.25, color=c[i-1], marker='.')


    lfont = {'fontname':'Source Serif Pro'}
    ax.set_xlabel('Time, s', **lfont)
    ax.set_ylabel('Voltage, V', **lfont)

    #ax.set_ylim([0,1])
    #ax.set_xlim(data['sim']['Time'][s],data['sim']['Time'][e])
    ax.grid(True, linestyle='dashed')

    try:
        if argv[2] == '-s':
            #plt.savefig(fname.split('.')[0]+'.pdf', dpi=300)
            #from matplotlib2tikz import save as tikz_save
            #tikz_save(fname.split('.')[0]+'.tex')
            pass
    except:
        pass

    plt.show()

if __name__ == "__main__":
    main(sys.argv)
