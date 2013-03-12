#!/opt/local/bin/python2
'''
The goal here is to unpreprocess the data from the MNIST database. It's too
consistent with the piece of frame the digit takes in the middle of the image.
I want to messy it up a bit to improve accuracy in the application.
'''

from __future__ import print_function
import pygame
import math

        
def make_surface_from(pixels):
    dim = int(math.sqrt(len(pixels)))
    surf = pygame.Surface((dim,dim))
    for y in range(dim):
        for x in range(dim):
            m = int(pixels[y * dim + x])
            surf.set_at((x, y), (m, m, m, 255))
    return surf
    
def pixel_datas():
    ''' Returns list. 1st element is answer, rest are pixels. '''
    with open('./data/original-data.csv', 'r') as fh:
        fh.readline()
        for line in fh.readlines():
            # Pixels are a 0-255 color rating, comma separated, for each
            # character in the rest of the line. 1 character -> 1 pixel.
            pixels = [int(x) for x in line.split(',')]
            yield pixels

def surface_as_pixels(surface):
    ''' Each pixel represented by 0-255 val '''
    pass
              
def resize(surface, factor):
    '''
    Is passed a pygame surface and resizes based on factor. Return new surface.
    '''
    assert (surface.get_width() == surface.get_height())
    dimension = surface.get_height()
    new_size = int(dimension + math.ceil(dimension * factor))
    dest = pygame.Surface((dimension, dimension))
    new_source = pygame.transform.scale(surface, (new_size, new_size))
    offset = -(0.5 * math.ceil(dimension * factor))
    dest.blit(new_source, (offset, offset))
    return dest

        
if __name__ == '__main__':
    
    # A fraction representing the change in size. 0.2 = 80% of original.
    resize_factor = 0.2
    
    for data in pixel_datas():
        surface = make_surface_from(data[1:])
        small_data = data[0].append(resize_smaller(surface, resize_factor))
        big_data = data[0].append(resize_larger(surface, resize_factor))
        assert (len(small_data) == len(big_data) == len(data))
        with open('./data/messy-data.csv', 'w') as fh:
            print(', '.join(data), file=fh)
            print(', '.join(small_data), file=fh)
            print(', '.join(big_data), file=fh)
            