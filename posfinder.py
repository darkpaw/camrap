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


# This class "decodes" grid pattern information from image data
# and compares it to the known grid pattern in order to determine 
# a position in grid coordinates.


import numpy
import Image, ImageDraw, ImageFont
import sys

if sys.platform == "win32":
    from time import clock
else:
    from time import time as clock

import os
import subprocess
import gridpattern

class positionfinder(object):


    def __init__(self):
        
        self.grid = gridpattern.gridpattern()

        self.grididx4x3 = {}
        
        g = self.grid.pattern
        
        for x in range(len(g[0]) - 4):
            for y in range(len(g) - 3):
                
                poskey = []
                
                for grid4x3x in range(4):
                    for grid4x3y in range(3):
                        poskey.append(repr(g[grid4x3y + y][grid4x3x + x]))
                
                key = "".join(poskey)
                print key
                self.grididx4x3[key] = (x,y,)
                print x,y, poskey
                
                
                
    
    def posfromkey(self, key):
        
        print key
        if self.grididx4x3.has_key(key):
            return self.grididx4x3[key]
        else:
            return None                 
                

    def findcentre(self, lines, imgsize):

        centrepx = imgsize / 2.0

        # find lines either side of centre

        rightline, leftline = None, None

        for idx,l in enumerate(lines):
            if l > centrepx:
                if idx > 0:
                    rightline = l
                    leftline = lines[idx-1]
                    break

        if rightline:

            #print "L: ", leftline
            #print "R: ", rightline

            gridwidthpx = rightline - leftline
            pxleftofcentre = centrepx - leftline
            #print "centring w, left of c, camcentre ", gridwidthpx, pxleftofcentre, centrepx
            leftfraction = pxleftofcentre / gridwidthpx

            return leftfraction

        return None     



    def findgridcells(self, hlines, vlines, pil_image):

        searchregions = []

        for vidx,v in enumerate(vlines):

            if len(vlines) > (vidx + 1):
                v2 = vlines[vidx + 1] 
            else:
                continue    

            searchcol = []
            searchregions.append(searchcol)

            for hidx,h in enumerate(hlines):

                if len(hlines) > (hidx + 1):
                    h2 = hlines[hidx + 1] 
                else:
                    break

                cell = ((vidx,hidx),(v,h,v2,h2))

                searchcol.append(cell)

        return searchregions


    def symbolfromimage(self, cellimg):
        
        grey = cellimg.sum(axis=2)
        #print "sfromi", grey.shape
        w = grey.shape[0]
        h = grey.shape[1]
        
        nwse = 0
        limit = min(w, h)
        
        if limit == 0:
            raise "invalid cellimg size"
        
        for x in range(limit):
            pix = grey[x, x]
            nwse += pix
        nwse = nwse / float(limit)    
#        print "nwse", nwse    
        if nwse < 300:
            return '1'
        
        nesw = 0
        for x in range(limit):
            pix = grey[limit - x - 1, x]
            nesw += pix
        nesw = nesw / float(limit)    
#        print "nesw", nesw    
        if nesw < 300:
            return '2'
        
        return '0'
        
        
        
    def getcellimages(self, cells, imgarray):

        #print imgarray 

        cellimages = [] 

        for column in cells:

            columncells = []
            
            for cell in column:

                #print "cell", cell

                cidx = cell[0]
                c = cell[1]
                w = c[2]-c[0]
                h = c[3]-c[1]

                #print h,w
                #take the middle 50% of full cell

                mgapw = int(w / 4.0)
                mgaph = int(h / 4.0)
                mw = int(w / 2.0)
                mh = int(h / 2.0)

                mx1 = c[0] + mgapw
                my1 = c[1] + mgaph
                mx2 = mx1 + mw
                my2 = my1 + mh

                #print mx1,my1,mx2,my2

                symbolpixels = imgarray[my1:my2:1,mx1:mx2:1,::]

                #symbolpixels = symbolpixels.sum(axis=2)  # greyscale
            
                columncells.append(symbolpixels)
        
            cellimages.append(columncells)
        
        return cellimages
     
