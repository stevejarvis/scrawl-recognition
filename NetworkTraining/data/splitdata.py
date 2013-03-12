#!/opt/local/bin/python2

from __future__ import print_function

with open('messy-data.csv', 'r') as fh:
    with open('test.csv', 'w') as testdata:
        for i in range(10000):
            print(fh.readline(), file=testdata, end='')            
    with open('train.csv', 'w') as traindata:
        for line in fh.readlines():
            print(line, file=traindata, end='')
