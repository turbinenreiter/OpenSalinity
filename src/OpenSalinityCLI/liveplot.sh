gnome-terminal --command="gnuplot -c plot.gp $1"
picocom /dev/ttyACM0 | tee $1
