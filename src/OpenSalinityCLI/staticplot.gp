#!/usr/bin/gnuplot -persist

set datafile separator " "

fname = ARG1

ftail = fname

plot ftail using 1:2 every ::1 with lines, ftail using 7:8 with lines
#, fname using 3:4 with lines, fname using 5:6 with lines, fname using 7:8 with lines, fname using 9:10 with lines, fname using 11:12 with lines, fname using 13:14 with lines, fname using 15:16 with lines
