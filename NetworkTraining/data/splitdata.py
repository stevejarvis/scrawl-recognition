#!/opt/local/bin/python2

from __future__ import print_function
import random

with open('messy-data.csv', 'r') as fh:
    all_data = fh.readlines()
    random.shuffle(all_data)
    with open('test.csv', 'w') as testdata:
        for i in range(50000):
            print(all_data[i], file=testdata, end='')            
    with open('train.csv', 'w') as traindata:
        for line in all_data[50000:]:
            print(line, file=traindata, end='')
