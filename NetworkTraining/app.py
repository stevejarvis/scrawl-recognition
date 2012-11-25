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

'''
The data we have currently is for 28x28 samples, possible dimensions for
section numbers (and neural net size) are:
4, 16, 49, 196, 784 total sections.
'''
SECTIONS = 49

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

def _learned(nn, num_sections, count_seen=None):
    ''' Determine if the network knows what's up yet. '''
    goal = .5
    total = 1000
    correct = 0
    with open('./data/test-no-header.csv', 'r') as fh:
        for i in range(total):
            line = fh.readline()
            pixels = [int(x) for x in line[2:].split(',')]
            inputs = sections_as_ink(_two_dimension(pixels), num_sections)
            res = nn.evaluate(inputs)
            print(res)
            # The results is just a list of outputs between -1 and 1.
            # Interpret as the index of the greatest output is the guess.
            ans = res.index(max(res))
            if int(line[0]) == ans:
                correct += 1
    percent = float(correct) / float(total)
    print('%d out of %d. %f percent.' %(correct, total, percent))
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

def train(nnet, num_sections, screen):
    ''' With chunks of data from the file, train the network. '''
    file_count = 0
    while not _learned(nnet, num_sections):
        print('\n***\nGone through the file %d times.\n***\n' %file_count)
        with open('./data/train-no-header.csv', 'r') as fh:
            data = []
            # Not at all resource friendly. If issues, use generator.
            for line_count, line in enumerate(fh.readlines()):
                # First character of each line is the answer digit.
                correct_index = int(line[0])
                ans = [3 if correct_index == i else -1 for i in range(10)]
                # Pixels are a 0-255 color rating, comma separated, for each
                # character in the rest of the line. 1 character -> 1 pixel.
                pixels = [int(x) for x in line[2:].split(',')]
                inputs = sections_as_ink(_two_dimension(pixels), num_sections)
                if screen and line_count % 100 == 0:
                    t = threading.Thread(target=_draw_things,
                                         args=(screen, pixels, inputs))
                    t.start()    
                    
                data.append((inputs, ans))
                # When we read in a good chunk of data, train.
                if line_count % 200 == 0:
                    nn.train_network(data, 
                                     change_rate=0.2,
                                     momentum=0.1, 
                                     iters=500)
                    if _learned(nnet, 
                                num_sections, 
                                (file_count * line_count + line_count)):
                        print('Made it!!')
                        import sys
                        sys.exit(0)
                    data = []
        file_count += 1
        
if __name__ == '__main__':
    visual_wanted = True
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
        
    num_hidden = SECTIONS
    nn = neuralnet.NeuralNetwork(SECTIONS, num_hidden, 10)
    
    train(nn, SECTIONS, screen)
