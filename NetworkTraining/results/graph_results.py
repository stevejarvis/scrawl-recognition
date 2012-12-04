#!/opt/local/bin/python2
'''
The network trainer wrote a bunch of performance data, now use that to make a
visual and see how everyone did.
'''

import sys
import matplotlib.pyplot as lab

# Optional path to log file, default 'performance.log'
try:
    logfile = sys.argv[1]
except IndexError:
    logfile = './performance.log'

# Data structure will be a dictionary. The keys will be the network/learning
# rate/momentum combos, the values will be lists of tuples, each (x,y) coords.
with open(logfile, 'r') as fh:
    dct = {}
    for line in fh.readlines():
        line = line.strip('\n')
        vals = line.split(' ')
        try:
            dct[vals[0]].append((vals[4], vals[5]))
        except KeyError:
            dct[vals[0]] = [(vals[4], vals[5])]

lab.title('Success rates over time with various networks.')
lab.xlabel('Training Iterations')
lab.ylabel('Success Percentage')
for k in dct.keys():
    xdata = []
    ydata = []
    for x, y in dct[k]:
        xdata.append(x)
        ydata.append(y)
    lab.plot(xdata, ydata, label=k)
lab.legend(loc=4)
lab.show()
