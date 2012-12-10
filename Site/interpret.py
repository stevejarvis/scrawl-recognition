#!/opt/local/bin/python2
'''
Website to which whatever is being drawn on should make requests.

Input: SIZE binary bits representing ink in image, stored in 'sec'.
    1 float for each extra percentage, 5 total, for NEWST.

Output: List of ranking of guesses and distance in likeliness from previous
spot. One per line.
E.g.:
8 0
3 0.12
7 0.54
...
'''

from __future__ import print_function
import cgi
import logging
import sys
# This is just to get neural-net in path on my dev machine
sys.path.append('/Users/steve/Dev/neuralnet')
import neuralnet

# Number of sections in image we're dealing with.
SIZE = 196
# Path to the root of the weights folder. Make sure this exists.
WEIGHTS_PATH = r'/Users/steve/Dev/scrawl/NetworkTraining/results/%s' %SIZE

# Set up the logger
logpath = './site.log'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=logpath,
                    filemode='a')
                        
# Print Header
print('Content-type: text/html\n')
print('<HTML>')

def find_best_weights(path):
    import os
    weights = os.listdir(path)
    if len(weights) == 0:
        print('Need to either train or fix weight path.')
        logging.error('No weights were at the weight path.')
        sys.exit(0)
    weights.sort()
    weights.reverse()
    return os.path.join(path, weights[0])
    
# Could use some error checking here
g = cgi.FieldStorage()
sections = list(g['sec'].value)
data = [int(x) for x in sections]
for param in ['t','n','s','w','e']:
    data.append(float(g[param].value))

logging.info('Data seems ok, got data: %s' %data)
    
nn = neuralnet.NeuralNetwork(SIZE + 5, SIZE + 5, 10)
nn.load_weights(find_best_weights(WEIGHTS_PATH))
logging.info('Weights loaded for %d network.' %SIZE)
res = nn.evaluate(list(data))

''' This output will need to be expanded upon. '''
print(res.index(max(res)))

# Close up
print('</HTML>')
