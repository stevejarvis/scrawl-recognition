#!/opt/local/bin/python2
'''
The network trainer wrote a bunch of performance data, now use that to make a
visual and see how everyone did.
'''

import sys
import matplotlib.pyplot as lab

def get_style_color(k):
    ''' Specific for values in app.py. Return tuple of (color, marker, label)
    Would be made better with regex, but... hack jack, hack.'''
    # This is specific. Pick a color
    if '16_' in k:
        style_a = 'g'
        label_a = '16, '
    elif '49_' in k:
        style_a = 'b'
        label_a = '49, '
    elif '196_' in k:
        style_a = 'r'
        label_a = '196, '
    elif '784_' in k:
        style_a = 'y'
        label_a = '784, '
    else:
        print('Size unknown!!')
        style_a = 'b'
        label_a = '*, '
    # And style
    if '0.2' in k:
        style_b = '^'
        label_b = '.2 learn, .1 mmnt'
    elif '0.002' in k:
        style_b = 's'
        label_b = '.002 learn, .001 mmnt'
    elif '0.00002' in k:
        style_b = 'o'
        label_b = '.00002 learn, .00001 mmnt'
    else:
        print('Learn rate unknown!!')
        style_b = '--'
        label_b = '*, *'
    return((style_a, style_b, '%s%s' %(label_a, label_b)))
        
# Optional path to log file, default 'performance.log'
try:
    logfile = sys.argv[1]
except IndexError:
    logfile = './performance.log'

# Data structure will be a dictionary. The keys will be the network/learning
# rate/momentum combos, the values will be lists of tuples, each (x,y) coords.
with open(logfile, 'r') as fh:
    dct = {}
    for linenum, line in enumerate(fh.readlines()): 
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
    col, mark, lbl = get_style_color(k)
    lab.plot(xdata, ydata, color=col, marker=mark, label=lbl)
lab.legend(loc=4)
lab.show()
