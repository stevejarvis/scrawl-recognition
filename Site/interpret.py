#!/opt/local/bin/python2
'''
Website to which whatever is being drawn on should make requests.

Input: SIZE binary bits representing ink in image, stored in 'sec'.
    1 float for each extra percentage, 5 total, for NEWST.

Output: json of list of tuples, guess and associated weight.
'''

from __future__ import print_function
import cgi
import logging
import sys
import json
# This is just to get neural-net in path on my dev machine
sys.path.append('/Users/steve/Dev/neuralnet')
import neuralnet

# Number of sections in image we're dealing with.
SIZE = 196
# Path to the root of the weights folder. Make sure this exists.
WEIGHTS_PATH = r'/Users/steve/Dev/scrawl/NetworkTraining/results/%s' %SIZE
# Because logging isn't gonna work so well in a real life web server.
DEBUG = False

if DEBUG:
	# Set up the logger
	logpath = './site.log'
	logging.basicConfig(level=logging.INFO,
						format='%(asctime)s %(levelname)s %(message)s',
						datefmt='%m-%d %H:%M',
						filename=logpath,
						filemode='a')
							
# Print Header
print('Content-type: text/html\n\n')

def find_best_weights(path):
    import os
    weights = os.listdir(path)
    if len(weights) == 0:
        print('Need to either train or fix weight path.')
		if DEBUG:
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

if DEBUG:
	logging.info('Data seems ok, got data: %s' %data)
    
nn = neuralnet.NeuralNetwork(SIZE + 5, SIZE + 5, 10)
nn.load_weights(find_best_weights(WEIGHTS_PATH))
if DEBUG:
	logging.info('Weights loaded for %d network.' %SIZE)
res = nn.evaluate(list(data))

output = [(res.index(weight), weight) for weight in res]
json.dumps(output.sort(key=lambda x: x[1]))
