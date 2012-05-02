
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


# This class loads the grid pattern data


class gridpattern(object):

    def __init__(self):
        

        f = open("pattern70x70.txt")
        
        pattern = []
        for line in f:
            
            if line.startswith('#'):
                continue
                
            if line.strip() == '' :
                continue
                   
            ints = map(int, line.strip())
            
            pattern.append(ints)
            
        self.pattern = pattern
