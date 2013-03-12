#!/opt/local/bin/python2
'''
The goal here is to unpreprocess the data from the MNIST database. It's too
consistent with the piece of frame the digit takes in the middle of the image.
I want to messy it up a bit to improve accuracy in the application.

The training application assumes 28x28 size, so this and the tests are designed
to suit.
'''

from __future__ import print_function
import pygame
import math

        
def make_surface_from(pixels):
    dim = int(math.sqrt(len(pixels)))
    assert dim == 28
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
    ''' Each pixel represented by 0-255 val. Return one long list, from top left
    to bottom right. '''
    # There are surfarray methods that may be faster, but insist on being 2 or
    # 3 dimensional. This is straight forward, albeit probably slow. It's a 
    # 1-time deal.
    assert (surface.get_width() == surface.get_height() == 28)
    dim = 28
    pixels = []
    for y in range(dim):
        for x in range(dim):
            # All 3 of RGB should be set identically.
            pixels.append(surface.get_at((x, y))[0])
    return pixels
              
def resize(surface, factor):
    '''
    Is passed a pygame surface and resizes based on factor. Return new surface.
    '''
    assert (surface.get_width() == surface.get_height())
    dimension = surface.get_height()
    dest = pygame.Surface((dimension, dimension))
    new_size = int(dimension + math.ceil(dimension * factor))
    new_source = pygame.transform.scale(surface, (new_size, new_size))
    offset = -(0.5 * math.ceil(dimension * factor))
    dest.blit(new_source, (offset, offset))
    return dest

def rotate(surface, degrees):
    '''
    Is passed a pygame surface and rotates based on degrees. Return new surface.
    Needs to be scaled back to 28x28, the rotated image will be slightly 
    smaller than original.
    '''
    assert (surface.get_width() == surface.get_height())
    new_surf = pygame.transform.rotate(surface, degrees)
    return pygame.transform.scale(new_surf, (28, 28))

        
if __name__ == '__main__':
    
    # A fraction representing the change in size. 0.2 = 80% of original.
    resize_factors = [0.0, 0.2, 0.3, 0.4, -0.2, -0.3, -0.4]
    # A positive rotation is counterclockwise, negative is clockwise. In degrees
    rotations = [0, 7, 12, -7, -12]
    data_path = r'/Users/steve/Dev/scrawl/NetworkTraining/data/messy-data.csv'
    
    with open(data_path, 'w'):
        # Start with empty file
        pass
    
    for data in pixel_datas():
        orig_surface = make_surface_from(data[1:])
        for size in resize_factors:
            sized_surface = resize(orig_surface, size)
            for rotation in rotations:
                end_surface = rotate(sized_surface, rotation)
                end_pixels = surface_as_pixels(end_surface)
                end_pixels.insert(0, data[0])
                assert (len(end_pixels) == len(data))
                with open(data_path, 'a') as fh:
                    print(','.join([str(i) for i in end_pixels]), file=fh)
        break
            