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


# This file contains the main loop of the application and application initialisation.
# 

import pygame, sys
import pygame.camera
from pygame.locals import *
import Image, ImageDraw, ImageFilter, ImageChops
import pixelsums, linedet, posfinder, displayareas, posaverages
import numpy


camresolutions =  (
    (320, 240) ,
    (352, 288) ,
    (640, 480),
    (800, 600), 
    (960, 544),
    (1024, 768), 
    (1280, 720), 
)

camres = camresolutions[2]
fullscreen = False
screenres = (1440,920)

# use n frames of position info. in averaging
AVG_WINDOW = 1

class mainloop(object):

    def __init__(self):


        pygame.init()
        pygame.camera.init()

        self.screen = pygame.display.set_mode(
            screenres,
            #pygame.FULLSCREEN    |
            pygame.DOUBLEBUF  |
            pygame.HWSURFACE   )  #| pygame.OPENGL 
        
        pygame.display.set_caption("Camrap")
        self.cam = pygame.camera.Camera("/dev/video0", camres)
        camrenderpos = (10,10)
        self.camrenderpos = camrenderpos 
        
        # display areas
        camrect = (camrenderpos[0],camrenderpos[1],camres[0]+camrenderpos[0],camres[1]+camrenderpos[1])
        xpostop = max(570, camrect[3] + 60)
        yposleft = max(570, camrect[2] + 60)
        
        self.camarea = displayareas.camarea(camrect, self.screen)
        self.vlinesarea = displayareas.vlinesarea((camrect[0],camrect[3], camrect[2], camrect[3]+50), self.screen)
        self.hlinesarea = displayareas.hlinesarea((camrect[2], camrect[1], camrect[2]+50, camrect[3]), self.screen)
        self.posareax = displayareas.positionareax((camrect[0], xpostop, camrect[0] + 500, xpostop + 60), self.screen)
        self.posareay = displayareas.positionareay((yposleft, camrect[1], yposleft + 100, camrect[1] + 500), self.screen)
        self.statusarea = displayareas.statusarea((camrect[2] + 10, camrect[3] + 60, camrect[2] + 310, camrect[3] + 250), self.screen)
        
        self.poslog = open("poslog.csv", 'w')
        

    def loop(self):


        self.cam.start()
        clock = pygame.time.Clock()
        #print dir(clock)
        ticks = 0l

        font = pygame.font.SysFont("Helvetica", 24)
        smallfont = pygame.font.SysFont("Helvetica", 12)

        sums = pixelsums.pixelsums()
        positioning = posfinder.positionfinder()
        linefinder = linedet.linedetection()	
        #pattern = readpattern.readpattern()

        avgs = posaverages.posaverages(AVG_WINDOW)

        showlines = True
        
        framecount = 0
        
        while 1:
            
            framecount += 1

            frametimes = []
            frametimes.append(("ST", 0, (0,120,120)))

            times = []
            t1 = pygame.time.get_ticks()

            #write_text(fpsmsg, screen, (4,4))

            image = self.cam.get_image()


            t2 = pygame.time.get_ticks() - t1
            #print "CP (capture):",  t2
            frametimes.append(("CP", t2, (255,0,0)))

            imgstring = pygame.image.tostring(image, "RGB")
            PILimg = Image.fromstring("RGB", camres, imgstring)
            imgasarray = numpy.asarray(PILimg)
            #imgasarray = pygame.surfarray.array3d(image)   # too slow...

            t2 = pygame.time.get_ticks() - t1
            #print "AR (img2array):",  t2
            frametimes.append(("AR", t2, (0,255,0)))

            # read h + v line averages
            linesums = sums.dosumsXY(imgasarray)
            
            t2 = pygame.time.get_ticks() - t1
            
            #print "SM:",  t2
            frametimes.append(("SM", t2, (0,0,255)))

            hsums = linesums[1]
            vsums = linesums[0]
            
            #~ t2 = pygame.time.get_ticks() - t1
            #~ print "AB:",  t2
            #~ frametimes.append(("AB", t2, (120,120,120)))

            if showlines:
                #print "show lines"				
                self.hlinesarea.showlines(hsums)			
                self.vlinesarea.showlines(vsums)	

            xlines = linefinder.read(hsums, 5)	
            self.hlinesarea.showlinetext(xlines)

            centrex = positioning.findcentre(xlines, camres[1])
            
                
            ylines = linefinder.read(vsums, 5)		

            self.vlinesarea.showlinetext(ylines)

            centrey = positioning.findcentre(ylines, camres[0])
            avgpos = avgs.logpos((centrey, centrex))

            if avgpos:
				xavg = avgpos[0]
				yavg = avgpos[1]        
            else:
				xavg = -9.99
				yavg = -9.99
				
            if framecount % 10 == 0:
                if centrex != None and centrex != None:
                    self.poslog.write("%0.7f, %0.7f\n" % (xavg, yavg))
                    #self.poslog.write("%0.7f, %0.7f\n" % (centrex, centrey))
            
                       
            cells = positioning.findgridcells(xlines, ylines, None)  #PILimg)

            self.camarea.showcam(image)  #screen.blit(image, camrenderpos)
            self.screen.fill((0,55,22), rect=(self.camrenderpos[0] + camres[0] / 2 - 1, self.camrenderpos[1] + (camres[1] / 2 - 25), 3, 50), special_flags=pygame.BLEND_ADD)            
            self.screen.fill((0,55,22), rect=(self.camrenderpos[0] + camres[0] / 2 - 25, self.camrenderpos[1] + (camres[1] / 2) - 1, 50, 3), special_flags=pygame.BLEND_ADD)            
   
            #print len(cells)
            centrecol = -1
            centrerow = -1
            ctrx = camres[0] / 2 
            ctry = camres[1] / 2 

            for colidx, col in enumerate(cells):
                
                    
                for rowidx, c in enumerate(col):
                    #print "ccc", c
                    cx = c[1][0]
                    cy = c[1][1]
                    cw = c[1][2] - c[1][0]
                    ch = c[1][3] - c[1][1]

                    if cx < ctrx and cx + cw > ctrx and cy < ctry and cy + ch > ctry:
                        centrecol = colidx
                        centrerow = rowidx
                        
                    self.screen.fill((0,28,0), rect=(cx+self.camrenderpos[0],cy+self.camrenderpos[1],cw,ch), special_flags =pygame.BLEND_ADD)
                    
                    
            #print "Centre in 4x3 grid >", centrecol, centrerow        
            
            cellimgs = positioning.getcellimages(cells, imgasarray)
            #print "cell images count:", len(cellimgs)
            self.screen.fill((0,0,0), rect=(self.posareay.x1 + 25, 15, 400, 700))

            poskey = []
            fail = False
                    
            for c, col in enumerate(cellimgs):
                
                if fail:
                    break
                
                if c > 3: 
                        break
                    
                for r, cellimg in enumerate(col):
                
                    if r > 2: 
                        break
                        
                    #print cellimg
                    drawpos = (self.posareay.x1 + 25 + c * 60, 15 + r * 65)
                    imgsurf = pygame.surfarray.make_surface(cellimg)
                    self.screen.blit(imgsurf, drawpos)
                    try:
                        symbol = positioning.symbolfromimage(cellimg)
                    except:
                        poskey = None
                        fail = True
                        break
                 
                    poskey.append(symbol)
                    symcolour = (250,255,0)
                    
                    if symbol == '2':
                        symcolour = (0,255,0)
                    if symbol == '1':
                        symcolour = (0,0,255)
                    if symbol == '0':
                        symcolour = (120,120,0)
            
                    self.screen.fill(symcolour, rect=(drawpos[0], drawpos[1], cellimg.shape[0], cellimg.shape[1]), special_flags=pygame.BLEND_ADD)
            
            if poskey:
                key = "".join(poskey)
                pos = positioning.posfromkey(key)
            else:
                pos = None
                
            fullcentrex = None
            fullcentrey = None
            
            if pos != None:
                #print "grid position>>>>> ", pos
                fullcentrey = pos[1] + xavg + centrerow# + xavg
                fullcentrex = pos[0] + yavg + centrecol# + yavg
                self.statusarea.showpos(fullcentrex, fullcentrey)

            else:
                #print "key not found:", key
                self.statusarea.showpos(-xavg, -yavg)

            # which column is centre in?
            
            if centrey != None:
                #ymsg = "Y: %0.4f grid units" % centrey
                self.posareay.showpos(avgs)
             
            if centrex != None:
                #xmsg = "X: %0.4f grid units" % centrex
                self.posareax.showpos(avgs)
            
        
            #t2 = pygame.time.get_ticks() - t1			
            #frametimes.append(("SY", t2, (0,120,120)))

            t2 =  pygame.time.get_ticks() - t1
            frametimes.append(("ZZ", t2, (120,120,120)))

            #print (centrex, centrey)
            #self.statusarea.showpos(centrex, centrey)

            clock.tick(30)
            ticks += 1

            t2 = pygame.time.get_ticks() - t1
            #print "SL (frame sleep):",  t2
            frametimes.append(("SL", t2, (255,255,0)))

            fpsmsg = "FPS %0.1f" % clock.get_fps()			
            self.statusarea.showFPS(fpsmsg)

            #self.statusarea.showtimes(frametimes)
            #self.statusarea.showpos(centrex, centrey)

            # display new frame
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.poslog.close()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit()
