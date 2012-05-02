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


# display areas handle screen regions for displaying information

import pygame

class displayarea(object):
    
    def __init__(self, rect, surf):
        
        self.rect = rect
        self.surf = surf
        self.x = rect[0]
        self.y = rect[1]
        self.x1 = rect[2]
        self.y1 = rect[3]
        self.font = pygame.font.SysFont("Helvetica", 24)
        self.smallfont = pygame.font.SysFont("Helvetica", 12)

    
    def clear(self):
        
        self.surf.fill((0,0,0), rect=(self.x,self.y, self.x1 - self.x, self.y1 - self.y))
    
        
    def write_text(self, text, pos, small=False):
            
        if small:
            ft = self.smallfont
        else:   
            ft = self.font
        text = ft.render(text, 1, (255, 255, 255), (0,0,0))
        textpos = text.get_rect()
        textpos.left = self.x + pos[0]
        textpos.top =  self.y + pos[1]
        self.surf.blit(text, textpos)
   
    
class positionareax(displayarea): 
    
    def __init__(self, rect, surf):
        
        displayarea.__init__(self, rect, surf)
                  
                  
        for i in range(11):
            surf.fill((255,0,0), rect=(self.x + 50 * i, self.y + 12,  1, 20), special_flags=0)
            self.write_text("%d" % i, (50 * i + 12, 0), True)
            
        for i in range(101):
            surf.fill((255,0,0), rect=(self.x + 5 * i, self.y + 22,  1, 10), special_flags=0)
      
    def showpos(self, avgs):
        
        if not avgs.prevxdigits:
            return
            
        #print "showpos", pos, self.x, self.y, self.x1, self.y1
        pos = avgs.xdigits[0]
        self.write_text("%0.5f" % pos, (522, 0), True)
        
        for d in range(4):
            pos = avgs.xdigits[d]
            prevpos = avgs.prevxdigits[d]
            self.surf.fill((0,0,20), rect=(self.x + prevpos * 500, self.y + 32 + d * 10, 2, 10), special_flags=0)
            self.surf.fill((0,220, 20), rect=(self.x + pos * 500, self.y + 32 + d * 10, 2, 10), special_flags=0)
        

class positionareay(displayarea): 
    
    def __init__(self, rect, surf):
        
        displayarea.__init__(self, rect, surf)
        
        width = self.x1 - self.x
                
        for i in range(11):
            self.write_text("%d" % i, (2, 2 + 50 * i), True)
            surf.fill((255,0,0), rect=(self.x + 12, self.y + 50 * i, 20, 1), special_flags=0)
            
        for i in range(100):
            surf.fill((255,0,0), rect=(self.x + 22, self.y + 5 * i, 10, 1), special_flags=0)
    
        
    def showpos(self, avgs):
        
        if not avgs.prevydigits:
            return
            
        width = self.x1 - self.x
        pos = avgs.ydigits[0]
        
        #print "showpos", pos, self.x, self.y, self.x1, self.y1
        self.write_text("Y %0.5f" % pos, (62, 0), True)

        for d in range(4):
            pos = avgs.ydigits[d]
            prevpos = avgs.prevydigits[d]
            self.surf.fill((0,0,20), rect=(self.x + 32 + d * 10, self.y + prevpos * 500, 10, 2), special_flags=0)
            self.surf.fill((0,220, 20), rect=(self.x + 32 + d * 10, self.y + pos * 500, 10, 2), special_flags=0)
            #self.surf.fill((0, 50, 255), rect=(1060 + d * 20, 20 + avgs.ydigits[d] * 1000, 16, 2), special_flags=0)
       

        #for d in range(4):
            #self.surf.fill((0,0,0), rect=(20 + self.prevxdigits[d] * 1000, 850 + d * 20, 2, 16), special_flags=0)
            #self.surf.fill((0,255, 50 * d), rect=(20 + self.xdigits[d] * 1000, 850 + d * 20, 2, 16), special_flags=0)
            ##screen.fill((0,255,255), rect=(850 + d * 20, 20 + xdigits[d] * 1000, 16, 2), special_flags=0)
            
        #for d in range(4):
            #screen.fill((0,0,0), rect=(1060 + d * 20, 20 + prevydigits[d] * 1000, 16, 2), special_flags=0)
            #screen.fill((0, 50 * d, 255), rect=(1060 + d * 20, 20 + ydigits[d] * 1000, 16, 2), special_flags=0)
       
    
class camarea(displayarea): 
    
    def __init__(self, rect, surf):
        
        displayarea.__init__(self, rect, surf)
        
    
    def showcam(self, image):
        
        self.surf.blit(image, (self.x, self.y))
        
        
    def showsymbol(self, symbol, pos):
        
        self.write_text(symbol, pos, True)
        
        

class vlinesarea(displayarea):  
    
    def __init__(self, rect, surf):
        
        displayarea.__init__(self, rect, surf)
        
    
    def showlines(self, linesums):
        
        self.clear()
        linesums = abs(linesums)
        minrowsum = min(linesums)
        maxrowsum = max(linesums)
    
        #print "Y lines", linesums[:50]
        for idx, rowsum in enumerate(linesums):
            scaled = (rowsum) / float(maxrowsum) * 50
            if(scaled > 0):
                self.surf.fill((0,255,0), rect=(self.x  + idx, self.y, 1, scaled))
                
    def showlinetext(self, lines):
    
        
        #~ ylinepaneltopleft = (camrenderpos[0] + camres[0] + 60,  camrenderpos[1])
        
        #~ screen.fill((0,0,0), rect=(ylinepaneltopleft,  (60, camres[1] + 20)))
        for line in lines:
            linemsg = "%0.2f" % line
            self.write_text(linemsg, (int(line) + 6, 5), True)
            #screen.fill((255,0,0), rect=(camrenderpos[0] + camres[0] + 5, camrenderpos[1] + idx,  scaled, 1))
                    

class hlinesarea(displayarea):  
    
    def __init__(self, rect, surf):
        
        displayarea.__init__(self, rect, surf)
        
    
    def showlines(self, linesums):
        
        self.clear()
        linesums = abs(linesums)
        #print linesums
        mincolsum = min(linesums)
        maxcolsum = max(linesums)
    
        #print minrowsum, maxrowsum
    
        for idx, colsum in enumerate(linesums):
            scaled = (colsum) / float(maxcolsum) * 50
            #print scaled
            if(scaled > 0):
                self.surf.fill((0,255,0), rect=(self.x, self.y + idx, scaled, 1))
    
    
    def showlinetext(self, lines):
    
        
        #~ ylinepaneltopleft = (camrenderpos[0] + camres[0] + 60,  camrenderpos[1])
        
        #~ screen.fill((0,0,0), rect=(ylinepaneltopleft,  (60, camres[1] + 20)))
        for line in lines:
            linemsg = "%0.2f" % line
            self.write_text(linemsg, (5, int(line) + 6), True)
            #screen.fill((255,0,0), rect=(camrenderpos[0] + camres[0] + 5, camrenderpos[1] + idx,  scaled, 1))
    
    

class statusarea(displayarea):  
    
    def __init__(self, rect, surf):
        
        displayarea.__init__(self, rect, surf)      
        
        self.runningavgvals = []
    
    def showFPS(self, fps):
        
        #print fps
        self.write_text(fps, (6, 6), False)
        
    def showpos(self, posx, posy):
        
        self.clear()
        
        if posx == None:
            return
        elif posy == None:
            return
        else:       
            xtext = "X %02.4f" % posx
            ytext = "Y %02.4f" % posy
        self.runningavgvals.append((posx,posy))
        self.write_text(xtext, (20, 30), False)
        self.write_text(ytext, (20, 64), False)
            
    def showtimes(self, times):
        
        prevtime = 0    
        
        for idx,t in enumerate(times):  
                        
            if idx > 1:                         
                widthms = t[1] - prevtime           
            else:                           
                widthms = t[1] 

            #print "TIME.......... ", widthms, t[0]             
            self.surf.fill(t[2], rect=(self.x + prevtime * 10, self.y + 60, widthms * 10, 30))
        
            msg = "%s %d" % (t[0], widthms)
            self.write_text(msg, (self.x + 2 + prevtime * 10, self.y + 62), True)
            prevtime = t[1]
            
            
