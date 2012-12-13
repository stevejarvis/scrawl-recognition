#!/usr/bin/python
'''
Website to which whatever is being drawn on should make requests.

Input: SIZE binary bits representing ink in image, stored in 'sec'.
    1 float for each extra percentage, 5 total, for NEWST.

Output: json of list of tuples, guess and associated weight.
'''

import cgi
import sys
import json
# Amend path on euclid
sys.path.append('/home/sjarvis/neural-network')
import neuralnet

# Number of sections in image we're dealing with.
SIZE = 196
# Path to the root of the weights folder. Make sure this exists.
WEIGHTS_PATH = r'/home/sjarvis/scrawl-recognition/NetworkTraining/results/%s' %SIZE
# Because logging isn't gonna work so well in a real life web server.
DEBUG = False
                           
# Print Header
print('Content-type: text/html\n\n')

def find_best_weights(path):
    import os
    weights = os.listdir(path)
    if len(weights) == 0:
        print('Need to either train or fix weight path.')
        if DEBUG:
            print('No weights were at the weight path.')
        sys.exit(0)
    weights.sort()
    weights.reverse()
    weight_path = os.path.join(path, weights[0])
    if DEBUG:
        print('found %s' %weight_path)
    return weight_path
    
# Could use some error checking here...
g = cgi.FieldStorage()
sections = list(g['sec'].value)
data = [int(x) for x in sections]
for param in ['t','n','s','w','e']:
    data.append(float(g[param].value))

if DEBUG:
    print('Data seems ok.')
    
nn = neuralnet.NeuralNetwork(SIZE + 5, SIZE + 5, 10)
try:
    nn.load_weights(find_best_weights(WEIGHTS_PATH))
except Exception, e:
    print('Error! Could not load weights, take blind guess. Error: %s' %e)
    sys.exit(0)

if DEBUG:
    print('Weights loaded for %d network.' %SIZE)
res = nn.evaluate(list(data))

output = [(index, weight) for index, weight in enumerate(res)]
output.sort(key=lambda x: x[1])
output.reverse()
print(json.dumps(output))
