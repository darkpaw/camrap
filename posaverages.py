#!/usr/bin/env python


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


# This class logs position data and can then return 
# averages of previous postion data.

class posaverages(object):

    def __init__(self, window):

        self.avglastpts = window
        self.prevpts = []

        self.xdigits = [0.5, 0.5, 0.5, 0.5, 0.5]
        self.ydigits = [0.5, 0.5, 0.5, 0.5, 0.5]

        #self.prevxdigits = list(self.xdigits)
        #self.prevydigits = list(self.ydigits)


    
    def logpos(self, pos):

        def trunc(f, n):
            '''Truncates/pads a float f to n decimal places without rounding'''
            slen = len('%.*f' % (n, f))
            return float(str(f)[:slen])
        
        if pos[0] == None:
            print "No position X"
            return None
        if pos[1] == None:
            print "No position Y"
            return None
            
        self.prevpts.append(pos)
        
        self.prevxdigits = list(self.xdigits)
        self.prevydigits = list(self.ydigits)
          
        xavg = 0.0
        yavg = 0.0
    
        
            
        if len(self.prevpts) >= self.avglastpts:   
            last = self.prevpts[-self.avglastpts:]
            for p in last:
                xavg += p[0]
                yavg += p[1]
        
            xavg = xavg / float(self.avglastpts)
            yavg = yavg / float(self.avglastpts)
            
            #print "pos logged:", xavg, yavg
            xdigits, ydigits = self.xdigits, self.ydigits
        
            
            xdigits[0] = xavg    
            xdigits[1] = abs(xavg - trunc(xavg, 1)) * 10
            xdigits[2] = abs(xavg - trunc(xavg, 2)) * 100
            xdigits[3] = abs(xavg - trunc(xavg, 3)) * 1000
            xdigits[4] = abs(xavg - trunc(xavg, 4)) * 10000
            
            ydigits[0] = yavg    
            ydigits[1] = abs(yavg - trunc(yavg, 1)) * 10
            ydigits[2] = abs(yavg - trunc(yavg, 2)) * 100
            ydigits[3] = abs(yavg - trunc(yavg, 3)) * 1000
            ydigits[4] = abs(yavg - trunc(yavg, 4)) * 10000
            
        return (xavg, yavg)
        
        #xmsg = " - avg. X: %0.6f" % xavg
        #write_text(xmsg, screen, (xlinepaneltopleft[0] + 120, xlinepaneltopleft[1] + 65), False)
        #ymsg = "- avg. Y: %0.6f" % yavg
        #write_text(ymsg, screen, (xlinepaneltopleft[0] + 120, xlinepaneltopleft[1] + 95), False)
        
    
    ##screen.fill((0,0,0), rect=(800, 20 + um * 1000, 16, 2), special_flags=0)
     
    
    ##for d in range(4):
        ##screen.fill((0,0,0), rect=(20 + prevxdigits[d] * 1000, 850 + d * 20, 2, 16), special_flags=0)
        ##screen.fill((0,255, 50 * d), rect=(20 + xdigits[d] * 1000, 850 + d * 20, 2, 16), special_flags=0)
        ###screen.fill((0,255,255), rect=(850 + d * 20, 20 + xdigits[d] * 1000, 16, 2), special_flags=0)
        
    ##for d in range(4):
        ##screen.fill((0,0,0), rect=(1060 + d * 20, 20 + prevydigits[d] * 1000, 16, 2), special_flags=0)
        ##screen.fill((0, 50 * d, 255), rect=(1060 + d * 20, 20 + ydigits[d] * 1000, 16, 2), special_flags=0)
   
    #prevxdigits = list(xdigits)            
    #prevydigits = list(ydigits)            
    
