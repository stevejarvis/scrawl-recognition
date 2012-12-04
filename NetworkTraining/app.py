#!/opt/local/bin/python
'''
Created on Sep 19, 2012

@author: steve

Tryin' to learn to recognize handwritten digits! 

Tricky, for this to work properly, the number of sections needs to be 
a perfect square and the root of it needs to be a divisor of the dimension.
Divisor so we fill each section with no leftovers, perf square because
we want to deal with a physical square.
'''

from __future__ import print_function
import neuralnet
import math
import time
import threading
import logging

'''
The data we have currently is for 28x28 samples, possible dimensions for
section numbers (and neural net size) are:
4, 16, 49, 196, 784 total sections.
'''
SECTIONS = 784

def _two_dimension(pixels):
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
            
def _section_contains_ink(lst, section_num, sections):
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
        if _section_contains_ink(values, x, sections):
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

def _learned(nn, num_sections, count_seen=None):
    ''' Determine if the network knows what's up yet. '''
    goal = .90
    total = 1000
    correct = 0
    with open('./data/test-no-header.csv', 'r') as fh:
        for i in range(total):
            line = fh.readline()
            pixels = [int(x) for x in line[2:].split(',')]
            two_d = _two_dimension(pixels)
            inputs = sections_as_ink(two_d, num_sections) + get_densities(two_d)
            res = nn.evaluate(inputs)
            # The results is just a list of outputs between -1 and 1.
            # Interpret as the index of the greatest output is the guess.
            ans = res.index(max(res))
            if int(line[0]) == ans:
                correct += 1
    percent = float(correct) / float(total)
    print('%s %d out of %d. %f percent.' %(threading.current_thread().name,
                                           correct, total, percent * 100))
    if count_seen != None:
        # Log the number of iterations and success rate
        logging.info('%d %d' %(count_seen, percent * 100))
    return percent >= goal

def _draw_things(screen, pixels, inked):
    ''' Just give a visual to verify data makes sense. '''
    # Paint it black
    screen.fill((0,0,0))
    # Draw the pixels
    ink = [(p,p,p) for p in pixels]
    for y in range(28):
        for x in range(28):
            pygame.draw.line(screen, ink[y * 28 + x], (x, y), (x, y))
    
    # Draw the sections
    sections_per_side = int(math.sqrt(SECTIONS))
    section_dimensions = 28 / sections_per_side
    for y in range(sections_per_side):
        for x in range(sections_per_side):
            ink_color = [inked[y * sections_per_side + x] * 255] * 3
            start_x = section_dimensions * x +56
            start_y = section_dimensions * y
            pygame.draw.rect(screen, 
                             ink_color, 
                             (start_x, start_y, 
                              section_dimensions, section_dimensions), 
                             0)
    pygame.display.flip()

def train(nnet, num_sections, screen, learn_rate, mom_rate):
    ''' With chunks of data from the file, train the network. '''
    file_count = 0
    while not _learned(nnet, num_sections) and file_count < 1:
        print('\n***\nGone through the file %d times.\n***\n' %file_count)
        with open('./data/train-no-header.csv', 'r') as fh:
            data = []
            # Not at all resource friendly. If issues, use generator.
            for line_count, line in enumerate(fh.readlines()):
                # First character of each line is the answer digit.
                correct_index = int(line[0])
                # Training to 1 & -1 yields results all very low.
                ans = [3 if correct_index == i else -1 for i in range(10)]
                # Pixels are a 0-255 color rating, comma separated, for each
                # character in the rest of the line. 1 character -> 1 pixel.
                pixels = [int(x) for x in line[2:].split(',')]
                two_d = _two_dimension(pixels)
                inputs = (sections_as_ink(two_d, num_sections) + 
                          get_densities(two_d))
                
                # If it's wanted and time, draw things.
                if screen and line_count % 100 == 0:
                    t = threading.Thread(target=_draw_things,
                                         args=(screen, pixels, inputs))
                    t.start()    
                    
                data.append((inputs, ans))
                # When we read in a good chunk of data, train.
                if line_count % 200 == 0:
                    nnet.train_network(data, 
                                     change_rate=learn_rate,
                                     momentum=mom_rate, 
                                     iters=200)
                    if _learned(nnet, 
                                num_sections, 
                                (file_count * line_count + line_count)):
                        print('Made it!! %s' %threading.current_thread().name)
                        # Better actually save these things!
                        nnet.save_weights(r'./results/%s_weights.txt' %threading.
                                        current_thread().name)
                        import sys
                        sys.exit(0)
                    data = []
        file_count += 1
        
if __name__ == '__main__':
    visual_wanted = False
    if visual_wanted:
        try:
            import pygame
        except ImportError:
            print('Cannot do visualizations without PyGame.')
            screen = None
        else:
            pygame.init()
            screen = pygame.display.set_mode((84, 28))
    else:
        screen = None
        
    nnet_sizes = [49, 196, 784]
    rates = [(0.002,0.001), (0.0005,0.0), (0.0001,0.00005)]
    
    logging.basicConfig(level=logging.INFO,
                        format='%(threadName)s %(asctime)s %(levelname)s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='./results/performance.log',
                        filemode='w')
    
    # Start threads doing magic
    threads = []
    for size in nnet_sizes:
        num_hidden = size + 5
        for learn, momentum in rates:
            # Make input 5 neurons larger to add pixel densities to the mix
            mnn = neuralnet.NeuralNetwork(size + 5, num_hidden, 10)
            # Start a thread with unique name so we can generate graphs
            # For each configuration from the log file.
            t = threading.Thread(target=train,
                                 name='%d_%f_%f' %(size, learn, momentum),
                                 args=(mnn, size, screen, learn, momentum))
            threads.append(t)
            t.start()
    print('%d threads doing science.' %len(threads))
