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

'''
The data we have currently is for 28x28 samples, possible dimensions for
section numbers (and neural net size) are:
4, 16, 49, or 196 total sections.
'''
SECTIONS = 16

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
    whether each section contained ink. '''
    results = []
    for x in range(sections):
        if _section_contains_ink(values, x, sections):
            results.append(1)
        else:
            results.append(0)
    return results

def _learned(nn, num_sections):
    ''' Determine if the network knows what's up yet. '''
    goal = .9
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

def train(nnet, num_sections):
    ''' With chunks of data from the file, train the network. '''
    while not _learned(nnet, num_sections):
        # This is not so good, only looking at first 100 lines every time.
        with open('./data/train-no-header.csv', 'r') as fh:
            data = []
            for i in range(100):
                line = fh.readline()
                correct_index = int(line[0])
                ans = [1 if correct_index == i else 0 for i in range(10)]
                pixels = [int(x) for x in line[2:].split(',')]
                inputs = sections_as_ink(_two_dimension(pixels), num_sections)
                data.append((inputs, ans))
            nn.train_network(data, iters=100)
        
if __name__ == '__main__':
    nn = neuralnet.NeuralNetwork(SECTIONS, SECTIONS, 10)
    train(nn, SECTIONS)
