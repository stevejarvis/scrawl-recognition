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

import neuralnet
import math
import time
import threading

'''
The data we have currently is for 28x28 samples, possible dimensions for
section numbers (and neural net size) are:
4, 16, 49, or 196 total sections.
'''
SECTIONS = 196

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
    if ret[0] > 200:
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

def _learned(nn, num_sections):
    ''' Determine if the network knows what's up yet. '''
    goal = .8
    total = 100
    correct = 0
    with open('./data/train-no-header.csv', 'r') as fh:
        for i in range(100):
            line = fh.readline()
            pixels = [int(x) for x in line[2:].split(',')]
            inputs = sections_as_ink(_two_dimension(pixels), num_sections)
            res = nn.evaluate(inputs)
            # The results is just a list of outputs between -1 and 1.
            # Interpret as the index of the greatest output is the guess.
            n = max(res)
            ans = [i for i, j in enumerate(res) if j == n]
            if int(line[0]) == ans[0]:
                correct += 1
    print('%d out of %d' %(correct, total))
    return correct / total >= goal

def _draw_things(screen, pixels, inked):
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
            color_index = y * sections_per_side + x
            print('index: %d value: %d' %(color_index, inked[color_index]))
            ink_color = [inked[color_index] * 255] * 3
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
    while not _learned(nnet, num_sections):
        with open('./data/train-no-header.csv', 'r') as fh:
            data = []
            # Not at all resource friendly. If issues, use generator.
            for line_count, line in enumerate(fh.readlines()):
                # First character of each line is the answer digit.
                correct_index = int(line[0])
                ans = [1 if correct_index == i else -1 for i in range(10)]
                # Pixels are a 0-255 color rating, comma separated, for each
                # character in the rest of the line. 1 character -> 1 pixel.
                pixels = [int(x) for x in line[2:].split(',')]
                inputs = sections_as_ink(_two_dimension(pixels), num_sections)
                if screen:
                    t = threading.Thread(target=_draw_things,
                                         args=(screen, pixels, inputs))
                    t.start()
                    # Just pause so I can decipher what this looks like.
                    time.sleep(5)
                data.append((inputs, ans))
                # We'll train on data sizes of 500
                if line_count % 500 == 0:
                    nn.train_network(data, momentum=0.8, iters=100)
                    data = []
        
if __name__ == '__main__':
    try:
        import pygame
        pygame.init()
        screen = pygame.display.set_mode((256, 128))
    except ImportError:
        print('Cannot do visualizations without PyGame.')
        screen = None
        
    # I read that a good number of hidden sections is the average of in & out.
    num_hidden = int((SECTIONS + 10) / 2)
    nn = neuralnet.NeuralNetwork(SECTIONS, num_hidden, 10)
    
    train(nn, SECTIONS, screen)
