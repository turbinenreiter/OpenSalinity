# OpenSalinity

The folder doc holds the Latex project that is the semester thesis.  

The folder src holds the source code and also the already gathered data. In src the folder vis holds a Python 3 script to plot the data.  
It is used like this:

```
cd ~\..\src\vis  
python3 vis.py <log-file> -s
```

log-file is the path to the log file. The log files are in the data directory within vis.  
-s saves the plot as svg. If -s is not called, an interactive plot is done instead.
