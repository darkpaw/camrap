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


# This class handles horizontal and vertical line detection.
# Row/column pixel sum data are averaged and then used to find "peaks" 
# of blackness. A parabola can be fitted to these peaks to give a 
# subpixel line position.


import numpy
import Image, ImageDraw, ImageFont
import sys

if sys.platform == "win32":
    from time import clock
else:
    from time import time as clock

import os
import subprocess


class linedetection(object):


    def __init__(self):

        pass

    def read(self, pixelsums, reject_edges_px):

        lines = self.findpeaks(pixelsums, reject_edges_px)
        return lines


    def findpeaks(self, linesums, reject):

        peaks = []
        peak = []
        prevpt = 0
        size = len(linesums)

        #print "find peaks", linesums[:20]

        for x, pt in enumerate(linesums):

            if pt > 20000.0:			
                
                #print x, pt
                
                if x - prevpt > 10:
                    peaks.append(peak)	
                    peak = []

                peak.append((x,pt))
                prevpt = x
                #print "pk x", x

        peaks.append(peak)
        #print peaks

        edgecleanedpeaks = []
        for peak in peaks:
            add = True
            for line in peak:				
                if line[0] <= reject:
                    add = False
                if line[0] >= (size - reject):
                    add = False

            if add:			
                edgecleanedpeaks.append(peak) 	

        peakfits = []

        for pk in edgecleanedpeaks:

            if len(pk) < 4:
                continue

            pkarr = numpy.asarray(pk)
            split = numpy.hsplit(pkarr,2)
            peakvals = split[1].sum(axis=1)
            xvals = split[0].sum(axis=1)
            #print "peak vals:", xvals
            fit = numpy.polyfit(xvals, peakvals, 2)
            peakfits.append((xvals,fit))		
            #print "peak fit:", fit

        #print peakfits

        lines = []

        for pkfit in peakfits:
            fit = pkfit[1]
            #print fit
            a = fit[0] 
            b = fit[1] 
            c = fit[2] 

            max = (- b) / (2 * a) 

            if(max < 0):
                #print max, pkfit
                #print edgecleanedpeaks
                pass
            else:
                lines.append(max)


        return lines
