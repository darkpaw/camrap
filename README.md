camrap
======

A 2d position encoding scheme for the reprap project

https://github.com/darkpaw/camrap

README stuff:

The camrap software is written for Python v2.7.

It will capture images of a printed grid with a webcam and report camera the X-Y location based on image analysis.

It needs some python libraries:

pygame numpy scipy PIL

On Ubuntu/Debian they can be installed with:

sudo apt-get install python-pygame python-numpy python-scipy python-imaging


Run it with:

python camrap.py

There are some options for resolution and averaging multiple frames at the top of mainloop.py

The "target" grid can be found in tools as 4mmA3.ps, it should print OK on A4 too.

