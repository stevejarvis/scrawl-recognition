'''
This is the main guy for training the handwriting recognition network.

There are 2 main functions: An experiment and general training.

The experiment is one designed to investigate the performance of different
network sizes and learning rates. It will print a nice graph (probably after a
few days!).

The other function is for training. It will just train and train, and whenever
the network as a personal best performance it will save the weights to:
./results/<network-size>/<ratio-correct>/<weights>

The most recent weights there should be used by the network in production.
'''

from __future__ import print_function
import sys
import os
import logging
import neuralnet
import threading
import random
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from image_ops import two_dimension, sections_as_ink, get_densities

def yell(msg):
    ''' Just because, if verbose, I want to print AND log. '''
    if verbose:
        print(msg)
    logging.info(msg)

def learned(nn, num_sections, num_samples=1000):
    ''' Return the ratio representing the success rate. '''
    correct = 0
    with open('./data/test.csv', 'r') as fh:
        for i in range(num_samples):
            line = fh.readline()
            pixels = [int(x) for x in line[2:].split(',')]
            two_d = two_dimension(pixels)
            inputs = (sections_as_ink(two_d, num_sections) + 
                      get_densities(two_d))
            res = nn.evaluate(inputs)
            # The results is just a list of outputs between -1 and 1.
            # Interpret as the index of the greatest output is the guess.
            ans = res.index(max(res))
            if int(line[0]) == ans:
                correct += 1
    return float(correct) / float(num_samples)

def get_training_data(sections):
    ''' Generator to give chunks of data. 
    There are 1.5M sets in the training data we have. '''
    with open('./data/train.csv', 'r') as fh:
        data = []
        # Not at all resource friendly. If issues, use generator.
        for line_count, line in enumerate(fh.readlines()):
            # First character of each line is the answer digit.
            correct_index = int(line[0])
            # Training to 1 & -1 yields results all very low.
            ans = [3 if correct_index == i else -1 for i in range(10)]
            # Pixels are a 0-255 color rating, comma separated, for each
            # character in the rest of the line. 1 character -> 1 pixel.
            pixels = [int(x) for x in line[2:].split(',')]
            two_d = two_dimension(pixels)
            inputs = (sections_as_ink(two_d, sections) + 
                      get_densities(two_d))
            data.append((inputs, ans))
            # When we read in a good chunk of data, give it up.
            if line_count % 500 == 0:
                yield data
                data = []
        
def train_experiment(nnet, num_sections, learn_rate, mom_rate, results=None):
    ''' This returns a list of tuples (iterations, success rate).
    Used for the experiment.'''
    iterations = 200
    if results == None:
        results = []
    for count, data in enumerate(get_training_data(num_sections)):
        nnet.train_network(data, 
                           change_rate=learn_rate,
                           momentum=mom_rate, 
                           iters=iterations)
        ratio = learned(nnet, num_sections)
        if verbose:
            print('%s %f percent after %d iterations.' 
                  %(threading.current_thread().name,
                    ratio * 100,
                    count * iterations))
        results.append((count * iterations, ratio))
    return results

def run_experiment():
    ''' This is the experiment that will generate graph for performance.'''
    try:
        import matplotlib.pyplot as lab
    except ImportError:
        yell('Need matplotlib for graphing.')
        sys.exit(0)
    
    yell('Running experiment...')
        
    def get_style_color(label):
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
            yell('Size unknown!!')
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
            yell('Learn rate unknown!!')
            style_b = '--'
            label_b = '*, *'
        return((style_a, style_b, '%s%s' %(label_a, label_b)))
     
    nnet_sizes = [16, 49, 196, 784]
    rates = [(0.2, 0.1), (0.002,0.001), (0.00002,0.00001)]
    dct = {}
    
    # Start threads doing magic
    threads = []
    for size in nnet_sizes:
        num_hidden = size + 5
        for learn, momentum in rates:
            label = '%d_%f_%f' %(size, learn, momentum)
            # Need a mutable structure to get back from the thread.
            dct[label] = []
            # Make input 5 neurons larger to add pixel densities to the mix
            mnn = neuralnet.NeuralNetwork(size + 5, num_hidden, 10)
            # Start a thread with unique name so we can generate graphs
            # For each configuration from the log file.
            t = threading.Thread(target=train_experiment,
                                 name=label,
                                 args=(mnn, size, learn, momentum, 
                                       dct[label]))
            threads.append(t)
            t.start()
    yell('%d threads doing science.' %len(threads))
    
    # Join those threads and get output
    for t in threads:
        t.join()
        
    # Now results should be full, graph away.
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

def get_weights(our_root):
    ''' Find best weights for size. 
    Return tuple (success rate, path to weights)'''
    try:
        options = os.listdir(our_root)
    except Exception:
        # Catching general exception because 2.7 throws "OSError" while
        # 3.3 throws "FileNotFoundError".
        os.mkdir(our_root)
        options = os.listdir(our_root)
    if options:
        options.sort()
        options.reverse()
        weights_path = os.path.join(our_root, options[0])
        yell('Found best weights at %s' %weights_path)
        # Trick. Can't have dots in paths, underscores are our placeholders.
        return (float(options[0].replace('_', '.')), weights_path)
    else:
        yell('Found no usable weights. Starting from scratch.')
        return (0.0, None)
      
def train_that_network(size):
    ''' I picture this running pretty much constantly. It should get updates
    on how well the network is doing, and if it's a PB, save the weights.'''
    # Start by finding the best weights we have so far for this size network.
    # Weights are in: ./results/<network-size>/<ratio-correct>/<weights>
    yell('Looking for best weights for %d neuron network.' %size)
    our_root = './results/%s/' %size
    current_best, weight_path = get_weights(our_root)
    mnn = neuralnet.NeuralNetwork(size + 5, size + 5, 10)
    if weight_path:
        mnn.load_weights(weight_path)
        yell('Weights loaded.')
    while True:
        # To avoid getting stuck from stagnant rates, pick from a couple at
        # random. This came to me in a daydream.
        learn_rate = random.choice([0.002, 0.0008, 0.0002])
        mmntm = learn_rate / random.choice([1.0, 2.0, 3.0])
        yell('Learning rate: %f Momentum rate: %f' %(learn_rate, mmntm))
        for data in get_training_data(size):
            mnn.train_network(data, learn_rate, mmntm, 300)
            ratio = learned(mnn, size, num_samples=49999)
            if ratio > current_best:
                percent_s = str(ratio).replace('.', '_')
                mnn.save_weights(os.path.join(our_root, percent_s))
                current_best = ratio
                yell('New best performance! %f percent right. Network size %d, Learning: %f.'
                     %(ratio * 100, size, learn_rate))
            else:
                if verbose:
                    print('Got a measley %f right.' %ratio)
       

if __name__ == '__main__':
    # Set up the logger
    logpath = './results/train_nnet.log'
    if not os.path.exists('./results'):
        os.makedirs('./results')
    logging.basicConfig(level=logging.INFO,
                        format='%(threadName)s %(asctime)s %(levelname)s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=logpath,
                        filemode='a')
    
    # Setup argument parser
    parser = ArgumentParser(description=('Choose options wisely... Logs at %s'
                                         %logpath), 
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('-e', '--experiment', 
                        dest='experiment', 
                        action='store_true', 
                        help='Generate graph of networks\' performance.\
                        Takes a long stinking time!')
    parser.add_argument('-t', '--train_size',
                        nargs=1,
                        help='Train a network. Supply size as argument.\
                        If nothing else is provided, this is required.')
    parser.add_argument('-v', '--verbose', 
                        dest='verbose', 
                        action='count',
                        default=0,
                        help='Spam yourself.')
    
    # Process arguments
    args = parser.parse_args()
    
    verbose = args.verbose > 0
    if verbose:
        yell('Verbose mode.')
    
    if args.experiment:
        run_experiment()
    else:
        try:
            size = int(args.train_size[0])
        except ValueError:
            print('Size must be an integer.')
            sys.exit(0)
        except TypeError:
            print('train.py -h for help.')
            sys.exit(0)
        if size not in [4, 16, 49, 196, 784]:
            print('Not a valid size! These are acceptable: 4, 16, 49, 196, 784.')
            sys.exit(0)
        train_that_network(size)
