#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np

with open('log_open_circuit_5000_samples.dat', 'r') as data_file:
    data = data_file.readlines()

i = 0
while i < len(data):
    data[i] = float(data[i].strip())
    i = i + 1

def analyze(length):
    mean = sum(data[:length])/len(data[:length])
    median = sorted(data[:length])[int(len(data[:length])/2)]
    mini = min(data[:length])
    maxi = max(data[:length])
    return [mean, median, mini, maxi]

mean_5k, median_5k, mini_5k, maxi_5k = analyze(5000)

slices_mean = []
slices_median = []
slices_mini = []
slices_maxi = []
error_mean = []
error_median = []

for i in range(1, len(data)):
    mean, median, mini, maxi = analyze(i)
    slices_mean.append(mean)
    slices_median.append(median)
    slices_mini.append(mini)
    slices_maxi.append(maxi)
    error_mean.append(abs(mean_5k - mean))
    error_median.append(abs(median_5k - median))

#n, bins, patches = plt.hist(data, maxi_5k-mini_5k, normed=1, facecolor='green', alpha=0.75)
#n, bins, patches = plt.hist(error_mean, maxi_5k-mini_5k, normed=1, facecolor='red', alpha=0.75)

#plt.plot(slices_mean)
#plt.plot(error_mean)
#plt.axhline(mean_5k)
plt.plot(data)

#plt.show()
plt.savefig('data.png')

#1 bit ADC -> /4096
