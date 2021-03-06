# OpenSalinity

doc - Latex files for the semester thesis  
src - source code  
data - all data gathered during experiments  
hardware - hardware design files  

## Software

The software for the microcontroller is developed using [MicroPython](micropython.org). The controller has to be flashed with the MicroPython firmware before it is able to run the Python scripts. Those Python scripts can be deployed on the microcontroller by copying them over to its filesystem which is present as flash drive when connected to a PC.  

The OpenSalinityGUI offers a simple user interface to capture and visualize data.  
![Hardware](doc/images/UI.png)

The OpenSalintyCLI shell script uses standard command line tools to do the same.  

DataPlot contains Python scripts to plot and analyze the gathered data.  
All software is licensed under the MIT-license.

## Hardware

In this project, the [Espruino Pico](espruino.com) development board was used, but other boards running MicroPython can replace it.  

Design files for the [MinieC](sparkyswidgets.com) and carrier board files are provided in the [eagle](cadsoft.io)-format.  

Gerbers for the electrode design are offerd as well.  
All hardware is licensed as CC-BY-SA-4.0  

![Hardware](compsys.jpg)
