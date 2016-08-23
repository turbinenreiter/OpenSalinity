---
title: Development of a Low-Cost Electrical Conductivity Meter for Liquids
author: Sebastian Plamauer
date: 22.08.2016
fontsize: 24pt
mainfont: Source Serif Pro
sansfont: Source Sans Pro
monofont: Source Code Pro
colortheme: biovt
---

# Outline

* Introduction
* Objectives
* Design
* Results
* Outlook

# Introduction

\begin{figure}
	\begin{center}
	\begin{tikzpicture}[scale=0.7]
		\node[,inner sep=0] at (0,0) {\includegraphics[width=\textwidth]{../thesis/images/pbr.jpg}};
		\draw[red!80!blue,ultra thick] (-5,1.5) ellipse (1.75 and 1.25);
		\draw[green!80!blue,ultra thick] (-2,-2) ellipse (3.25 and 2.25);
		\draw[-latex, blue!80!white, ultra thick] (-0.9,1.1) -- (2,1.15);
		\draw[-latex, blue!80!white, ultra thick] (2.25,-0.45) -- (0.85,-0.8);
		\draw[-latex, blue!80!white, ultra thick] (4.5,1) .. controls (5,0.75) and (4.5,0) ..  (3.75,-0.15);
	\end{tikzpicture}
		%\caption[The photobioreactor for which the conductivity meter is developed]{The photobioreactor for which the conductivity meter is developed - Water enters through the inlet basin, (\drawline[red!80!blue]), streams down the ramp (\drawline[blue!80!white,-latex]) to the collection tank (\drawline[green!80!blue]) from where it is pumped back to the inlet.}
		\label{fig:pbr}
	\end{center}
\end{figure}

# Objectives

enable experiments to validate simulation

* add saltwater impulse to freshwater stream
* measure changes in salinity over time
    * at multiple points
    * fast

---------------

## Requirements

* spacial resolution:   10mm
* sensitivity:          0.1%
* range:                0 to 2.5%
* cost per sensor:      < €25
* deployable in the algae reactor
* easy to use

# Design

\begin{figure}
	\begin{center}
\begin{tikzpicture}[scale=0.65]
	\fill [fill=yellow, opacity=0.25] (-5.5,4) rectangle (5.2,7);
	\fill [fill=green, opacity=0.25] (-5.5,-3.5) rectangle (5.2,4);
	\fill [fill=blue, opacity=0.25] (5.2,-3.5) rectangle (10,2);
	\begin{pgfonlayer}{nodelayer}
		\node [rounded corners=8pt, inner sep=8pt, style=rect] (0) at (8, -1) {8 Electrodes};
		\node [rounded corners=8pt, inner sep=8pt, style=rect] (1) at (0, 3) {Microcontroller};
		\node [rounded corners=8pt, inner sep=8pt, style=rect] (2) at (-3, -1) {MinieC Interface};
		\node [rounded corners=8pt, inner sep=8pt, style=rect] (3) at (3, 0.25) {Matrix Switch};
		\node [rounded corners=8pt, inner sep=8pt, style=rect] (4) at (0, 6) {PC};
		\node [style=rect, inner sep=8pt, rounded corners=8pt] (5) at (3, -2.25) {Matrix Switch};
	\end{pgfonlayer}
	\begin{pgfonlayer}{edgelayer}
		\draw [style=darrow] (4) to node[left]{USB} (1);
		\draw [style=simple, bend right=15, looseness=1.00] (0) to node[above]{8 SIG} (3);
		\draw [style=simple, bend right=15, looseness=1.00] (3) to node[above]{SIG} (2);
		\draw [style=arrow, bend left=15, looseness=1.00] (1) to node[right]{SPI} (3);
		\draw [style=darrow, bend right=15, looseness=1.00] (1) to node[left]{I2C} (2);
		\draw [style=simple, bend right=15, looseness=1.00] (2) to node[below]{GND} (5);
		\draw [style=simple, bend right=15, looseness=1.00] (5) to node[below]{8 GND} (0);
		\draw [style=arrow, bend left=15, looseness=1.00] (1) to node[right, pos=0.9]{SPI} (5);
	\end{pgfonlayer}
		\draw (-5.5,-3.5) -- (10,-3.5) -- (10,2) node[below, left, yshift=-8pt] {$n$} -- (-5.5,2) -- (-5.5,-3.5);
\end{tikzpicture}
		%\input{images/system_design.tikz}
		%\includegraphics[width=\textwidth]{images/systemdesign.pdf} 
		%\caption[System Design]{System Design - The yellow area marks the user interface of the system, the green area is the hardware that is mounted on the carrier board and the blue area shows the sensors deployed in the water stream. The rectangle marks the parts of the system that is repeated $n$ times to get to the needed number of sensors.}
		\label{fig:sys}
	\end{center}
\end{figure}

---------------

## finished Hardware

\begin{figure}
	\begin{center}
		\begin{tikzpicture}[scale=0.7]
			\node[,inner sep=0] at (0,0) {\includegraphics[width=0.5\textwidth]{../thesis/images/cb.jpg}};
			\node[inner sep=0] at (0,-3) {\includegraphics[width=\textwidth]{../thesis/images/fpcbp.jpg}};
			
			\draw[red,ultra thick,rounded corners] (-4,-0.75) rectangle (-1.5,0.75);
			
			\draw[red!40!yellow,ultra thick,rounded corners] (-1,-0.35) rectangle (-0.25,0.35);
			\draw[red!40!yellow,ultra thick,rounded corners] (0.55,-0.35) rectangle (1.3,0.35);
			
			\draw[red!25!yellow,ultra thick,rounded corners] (-1.45,-1) rectangle (-0.3,-0.6);
			\draw[red!25!yellow,ultra thick,rounded corners] (0.3,-1.05) rectangle (1.3,-0.65);
			\draw[red!25!yellow,ultra thick,rounded corners] (-1.54,1.05) rectangle (-0.44,0.65);
			\draw[red!25!yellow,ultra thick,rounded corners] (0.15,1.05) rectangle (1.15,0.65);
			
			\draw[blue,ultra thick,rounded corners] (1.8,-1.2) rectangle (4,1.2);
			\draw[green,ultra thick,rounded corners] (-8,-4) rectangle (8,-2);
			\draw[blue!50!white,ultra thick,rounded corners] (-2.75,-3.5) rectangle (-1.65,-2.5);
		\end{tikzpicture}
		%\caption[The developed sensor system]{The developed sensor system - The microcontroller and USB connection (\drawline[red,ultra thick]) control all parts and connect to the host PC. The matrix switches (\drawline[red!40!yellow,ultra thick]) connect the MinieC (\drawline[blue,ultra thick]) to the sensor strip (\drawline[green,ultra thick]) containing the sensors (\drawline[blue!50!white,ultra thick]) via the connectors (\drawline[red!25!yellow,ultra thick]).}
		\label{fig:isys}
	\end{center}
\end{figure}

<!--```python-->
<!--import main-->

<!--print('test')-->
<!--```-->

# Results

---------------

## Demo

# Outlook

\begin{figure}
    \begin{center}
        \includegraphics[height=225pt]{images/wing.pdf}
    \end{center}
\end{figure}
