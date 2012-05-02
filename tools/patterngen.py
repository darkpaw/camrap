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



import random
import string

chars = ['0', '1', '2']

width = 70
height = 70

def rand_char():
	
	r = random.randint(0,32000)
	c = chars[r % 3]
	return c

lines = []
for x in range(0, width):
	#print
	line = []
	for y in range(0, height):
		
		c = rand_char()
		#print c,
		line.append(c)
	lines.append(line)


count = 0
dupe_count = 99

while dupe_count > 0:
		
	dupe_count = 0
	count = 0
	words = {}
	
	for x in range(0, width - 3):
		
		for y in range(0, height - 4):
			word = []
			word += lines[x+0][y]
			word += lines[x+1][y]
			word += lines[x+2][y]
			word += lines[x+0][y+1]
			word += lines[x+1][y+1]
			word += lines[x+2][y+1]
			word += lines[x+0][y+2]
			word += lines[x+1][y+2]
			word += lines[x+2][y+2]
			word += lines[x+0][y+3]
			word += lines[x+1][y+3]
			word += lines[x+2][y+3]
			
			wordstr = string.join(word)
			
			if(words.has_key(wordstr)):
				
				lines[x+0][y] = rand_char()
				lines[x+1][y] = rand_char()				
				lines[x+2][y] = rand_char()		
				dupe_count += 1
				#print "dupe", wordstr
			else:
				words[wordstr] = 1	
			
			count += 1
			
	print "#, # dupes", count, dupe_count		
	
	
f = open("trinary_out.txt", 'wt')
for y, line in enumerate(lines):
	print string.join(line, '') 
	f.write(string.join(line, '') + '\n')
	
f.close()	

		
		
