
print """%!PS-Adobe-1.0 
%%BoundingBox: -1 -1 576 432  
%%EndComments 
%%EndProlog 
gsave 
 
/f {findfont exch scalefont setfont} bind def 
/s {show} bind def 
/ps {true charpath} bind def 
/l {lineto} bind def 
/m {newpath moveto} bind def 
matrix currentmatrix /originmat exch def 
/umatrix {originmat matrix concatmatrix setmatrix} def 
 
0 0 m 
[] 0 setdash 
0.1 setlinewidth 
0 0 0 setrgbcolor 

/Times-Roman findfont
10 scalefont
setfont

%/mm { 72 mul 25.4 div } bind def
/mm { 72 mul 30 div } bind def

"""



# a4 = 297 * 210 mm   842 595 points

#0 0 moveto
import math

max_x = 210
max_y = 297

#mins
xmargin = 5
ymargin = 5


yrange = (ymargin, max_y - ymargin)
xrange = (xmargin, max_x - xmargin)

width_mm = 2

colour = True


#print hexside, hexup, hexacr

print """
/drawsquare0 {
   newpath
   m
   0 0 0 setrgbcolor
"""   
print "   0 mm %.3f mm rlineto" % width_mm
print "   %.3f mm 0 mm rlineto" % width_mm
print "   currentpoint"
print "   stroke"

print "   } def"


print """
/drawsquare1 {
   newpath
   m
   0 0 0 setrgbcolor
"""   
print "   0 mm %.3f mm rlineto" % width_mm
print "   %.3f mm 0 mm rlineto" % width_mm
print "   -%.3f mm -%.3f mm rmoveto" % (width_mm * 0.375, width_mm * 0.375)
print "   currentpoint"
print "   stroke"
print "   0.12 mm 0 360 arc"
print "   currentpoint"
print "   -%.3f mm -%.3f mm rmoveto" % (width_mm * 0.25, width_mm * 0.25)
print "   currentpoint"
print "   0.12 mm 0 360 arc"
print "   currentpoint"
print "   fill"

#306 396 144 0 360 arc closepath fill
print "   } def"



# working ps dots

#~ /drawsquare1 {
#~ newpath
#~ m
#~ 0 0 0 setrgbcolor

#~ 0 mm 2.000 mm rlineto
#~ 2.000 mm 0 mm rlineto
#~ %stroke
#~ -0.75 mm -0.75 mm rmoveto
#~ currentpoint
#~ stroke

#~ 0.1 mm 0 360 arc
#~ currentpoint
#~ %fill

#~ -0.5 mm -0.5 mm rmoveto
#~ currentpoint
#~ 0.1 mm 0 360 arc
#~ currentpoint
#~ fill

#~ %0.1 mm 0 360 arc
#~ %fill

#~ %currentpoint

#~ } def



print """
/drawsquare2 {
   newpath
   m
   0 0 0 setrgbcolor
"""   
print "   0 mm %.3f mm rlineto" % width_mm
print "   %.3f mm 0 mm rlineto" % width_mm
print "   -%.3f mm -%.3f mm rmoveto" % (width_mm * 0.625, width_mm * 0.375)
print "   currentpoint"
print "   stroke"
print "   0.12 mm 0 360 arc"
print "   currentpoint"
print "   %.3f mm -%.3f mm rmoveto" % (width_mm * 0.25, width_mm * 0.25)
print "   currentpoint"
print "   0.12 mm 0 360 arc"
print "   currentpoint"
print "   fill"


print "   } def"



# 

#import random

xgrids = 70
ygrids = 70

f = open("pattern70x70.txt")

lines = []

for line in f:
	
	lines.append(line)

digits = [0,1,2]
	
for x in range(0, xgrids):
		for y in range(0, ygrids):
			
			pos_x = xmargin + x * width_mm
			pos_y = ymargin + y * width_mm
			digit = int(lines[x][y])
			
			print "%.3f mm %.3f mm drawsquare%d " % (pos_x, pos_y, digit)


print """


showpage 
grestore 
%%Trailer""" 
