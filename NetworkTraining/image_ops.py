#!/opt/local/bin/python
'''
Created on Sep 19, 2012

@author: steve

Tryin' to learn to recognize handwritten digits! 

Tricky, for this to work properly, the number of sections needs to be 
a perfect square and the root of it needs to be a divisor of the dimension.
Divisor so we fill each section with no leftovers, perf square because
we want to deal with a physical square.

The data we have currently is for 28x28 samples, possible dimensions for
section numbers (and neural net size) are:
4, 16, 49, 196, 784 total sections.

This module is just functions used to manipulate the image.
'''

from __future__ import print_function
import math

def two_dimension(pixels):
    ''' Pixels must be a perfect square. Access by twod[y][x] '''
    assert math.sqrt(len(pixels)) % 1 == 0
    side = int(math.sqrt(len(pixels)))
    twod = []
    for y in range(side):
        row = []
        for x in range(side):
            row.append(pixels[y * side + x])
        twod.append(row)
    return twod
            
def section_contains_ink(lst, section_num, sections):
    ''' Get list, section number in question, and total sections, 
    return whether any pixel in that section is over the threshold. '''
    sections_per_side = math.sqrt(sections)
    section_dimension = len(lst) / sections_per_side
    assert section_dimension % 1 == 0 and sections_per_side % 1 == 0
    start_row = int(math.floor(section_num / sections_per_side) * 
                    section_dimension)
    start_col = int(math.floor(section_num % sections_per_side) * 
                    section_dimension)
    ret = []
    for y in range(start_row, int(start_row + section_dimension)):
        for x in range(start_col, int(start_col + section_dimension)):
            ret.append(lst[y][x])
    ret.sort()
    ret.reverse()
    # Change the threshold here
    if ret[0] > 245:
        return True
    return False

def sections_as_ink(values, sections):
    ''' This is how we want to represent the data. Given all the pixel values,
    think of them as sections and return a list of binary values. Only represent
    whether each section contained ink.
    
    Picture read from left to right, top to bottom, put in linear list. '''
    results = []
    for x in range(sections):
        if section_contains_ink(values, x, sections):
            results.append(1)
        else:
            results.append(0)
    return results

def get_densities(values):
    ''' Pass the pixels in a 2d list.
    Return a list of 5 values representing pixel distribution in the image.
    Total % pixels "on", % north of half, % south of half, % left of half, % 
    right of half. '''
    total = north = south = west = east = 0
    threshold = 245
    # Get north count
    for y in range(14):
        for x in range(28):
            if values[y][x] >= threshold:
                north += 1
    # Get south
    for y in range(14, 28):
        for x in range(28):
            if values[y][x] >= threshold:
                south += 1
    # West
    for y in range(28):
        for x in range(14):
            if values[y][x] >= threshold:
                west += 1   
    # East
    for y in range(28):
        for x in range(14,28):
            if values[y][x] >= threshold:
                east += 1
    
    total = north + south + west + east
                
    vals = [float(x) / float(784) for x in [total, north, south, west, east]]
    # Need to expand these values a bit. Get some space!
    vals = [x * 10 for x in vals]
    return vals