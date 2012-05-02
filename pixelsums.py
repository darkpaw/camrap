# Copyright 2012 Felix Sheldon
#
# This file is part of Camrap.
#
# Camrap is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version.
#
# Camrap is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Camrap. If not, see http://www.gnu.org/licenses/.
#


# This class sums pixel values in rows and columns, and detrends 
# the data to account for non-uniform lighting.


import numpy
import Image, ImageDraw, ImageFont
import sys
#import handythread

if sys.platform == "win32":
    from time import clock
else:
    from time import time as clock

#import os
#import subprocess

#from multiprocessing import Pool

class pixelsums(object):


    def __init__(self):

        pass

    def dosumsXY(self, image_array):

        t = clock()
        self.image_array = image_array

        #horsums, versums = self.sum_multi()

        horsums, versums = self.sum_numpy()

        #print  "numpy sums %0.3f" % (clock() - t)

        hdetrended, vdetrended = self.findlinesums(horsums, versums)

        #print  "detrend %0.3f" % (clock() - t)

        return hdetrended, vdetrended


    def sum_numpy(self):

        #~ greypixels = self.image_array.sum(axis=2)
        #~ vertsums = greypixels.sum(axis=0)
        #~ horsums = greypixels.sum(axis=1)

        # faster	
        vertsums = abs(self.image_array.sum(axis=0).sum(axis=1))
        horsums = abs(self.image_array.sum(axis=1).sum(axis=1))

        return horsums, vertsums

    def sum_multi(self):

        def sum_ax0(array):

            return array.sum(axis=0)

        def sum_ax1_window(array_window):

            array = array_window[1]
            x = array_window[0][0]
            x2 = array_window[0][1]

            sliced = array[x:x2]
            #print "Sliced: ",len(sliced), sliced
            sums = sliced.sum(axis=1)
            #print "sums:", len(sums), sums
            return sums


        greypixels = self.image_array.sum(axis=2)
        greyv = greypixels.transpose()

        xwindows = range(0,greyv.shape[0], 20)		
        width = greyv.shape[0]
        jobs = []
        for idx, w in enumerate(xwindows):
            if(idx > 0):
                job = ((xwindows[idx-1], w), greyv)
                jobs.append(job)
        if w < width:	
            job = ((w, width), greyv)
            jobs.append(job)

        multi_sums = handythread.parallel_map(sum_ax1_window,jobs,threads=16)

        xsums= []
        map(xsums.extend, multi_sums) 



        ywindows = range(0,greypixels.shape[0], 20)		
        width = greypixels.shape[0]
        jobs = []
        for idx, w in enumerate(ywindows):
            if(idx > 0):
                job = ((ywindows[idx-1], w), greypixels)
                jobs.append(job)
        if w < width:	
            job = ((w, width), greypixels)
            jobs.append(job)

        multi_sums = handythread.parallel_map(sum_ax1_window,jobs,threads=16)

        ysums= []
        map(ysums.extend, multi_sums) 

        return ysums, xsums


    def findlinesums(self, horsums, vertsums):	

        xsize = self.image_array.shape[1]
        ysize = self.image_array.shape[0]

        xaxis = numpy.arange(ysize)
        yaxis = horsums

        fit = numpy.polyfit(xaxis,yaxis,3)

        ydetrended = numpy.zeros(ysize, dtype=int)
        #fitplot = numpy.zeros(ysize, dtype=int)

        for x in xaxis:
            yval = int(fit[0] * x**3 + fit[1] * x**2 +fit[2] * x + fit[3])
            ydetrended[x] = horsums[x] - yval
            #fitplot[x] = yval

        ydetrended = ydetrended.clip(-999000, -7000)	

        xaxis = numpy.arange(xsize)
        yaxis = vertsums

        fit = numpy.polyfit(xaxis,yaxis,3)

        xdetrended = numpy.zeros(xsize, dtype=int)

        #fitplot = numpy.zeros(xsize, dtype=int)

        for x in xaxis:
            yval = int(fit[0] * x**3 +fit[1] * x**2 + fit[2] * x + fit[3])
            xdetrended[x] = vertsums[x] - yval
            #fitplot[x] = yval

        xdetrended = xdetrended.clip(-999000, -7000)	



        return abs(xdetrended), abs(ydetrended)
