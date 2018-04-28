import numpy as np
import random
from math import log
import sys
import DES


#
# Get number of tests
#
num_of_test = 0
with open('num_tests.txt') as f:
    num_of_test = int(f.read())



#
# Loop configurations files
#
for file_index in range(1, num_of_test + 1):

    mode_file = 'mode_' + str(file_index) + '.txt'
    para_file = 'para_' + str(file_index) + '.txt'
    arrival_file = 'arrival_' + str(file_index) + '.txt'
    service_file = 'service_' + str(file_index) + '.txt'


    #
    # Get mode
    #
    mode = ''
    with open(mode_file) as f:
        mode = f.read()

    mode = mode.strip()

    #
    # Get parameters
    #
    para = ''
    with open(para_file) as f:
        para = f.read()

    para = para.split('\n')
    para = [i.strip() for i in para]
    para = [i for i in para if i != '']
    para = [float(i) for i in para]

    #
    # Get arrival
    #
    arrival = ''
    with open(arrival_file) as f:
        arrival = f.read()

    arrival = arrival.split('\n')
    arrival = [i.strip() for i in arrival]
    arrival = [i for i in arrival if i != '']
    arrival = [float(i) for i in arrival]

    #
    # Get service
    #
    service = ''
    with open(service_file) as f:
        service = f.read()

    service = service.split('\n')
    service = [i.strip() for i in service]
    service = [i for i in service if i != '']
    service = [float(i) for i in service]



 
    
    if mode == 'trace':
        
        DES.trace_mode(arrival, service, int(para[0]), para[1], para[2], file_index)

    elif mode == 'random':
        
        DES.random_mode(arrival[0], service[0], int(para[0]), para[1], para[2], para[3], file_index)
        
        
    
    
    
    
    
    
