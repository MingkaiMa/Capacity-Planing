import numpy as np
import random
from math import log
Inf = float('inf')

def random_mode(arrival, service, m, setup_time, delayedoff_time, time_end):


    response_time_cumulative = 0
    num_customer_served = 0
    
    #
    # mean arrival rate
    lam = arrival
    #
    # mean service time
    mu = service
    

    next_arrival_time = -log(1 - random.random()) / lam
    service_time_next_arrival = -log(1 - random.random()) / mu + (-log(1 - random.random()) / mu) + (-log(1 - random.random()) / mu)

    next_departure_time = Inf * np.ones((m, 1))


    departure_info = []
    response_time_record = []
    master_clock = 0

    #
    # A server may have four states:
    # 0: OFF
    # 1: SETUP
    # 2: BUSY
    # 3: DELAYEDOFF
    # initial states for all servers are 0: OFF
    server_state = np.zeros((m, 1))

    arrival_time_next_departure = np.zeros((m, 1))
    
    #
    # set up time for servers
    set_up_time_for_server = Inf * np.ones((m, 1))
    #
    # delayedoff timer for servers
    delayedoff_timer_for_server = Inf * np.ones((m, 1))
    
    buffer_content = []
    queue_length = 0

    while master_clock < time_end:

        first_departure_time = np.min(next_departure_time)
        first_departure_server = np.argmin(next_departure_time)

        first_setup_finish_time = np.min(set_up_time_for_server)
        first_setup_finish_server = np.argmin(set_up_time_for_server)

        first_countdown_to_turnoff_time = np.min(delayedoff_timer_for_server)
        first_countdown_to_turnoff_server = np.argmin(delayedoff_timer_for_server)
        
        # 
        #
        # Find out whether the next event is an arrival or depature
        #
        # 0: departure
        # 1: arrival
        # 2: setup finished, take a marked job from queue, state from setup to busy
        # 3: countdown finished, needs to turn off,  state from delayedoff to off
        #

        # At the beginning, an arrival
        if first_departure_time == Inf and first_setup_finish_time == Inf and first_countdown_to_turnoff_time == Inf:
            next_event_time = next_arrival_time
            next_event_type = 1

        # departure time first
        elif first_departure_time < first_setup_finish_time and first_departure_time < first_countdown_to_turnoff_time:        
            if next_arrival_time < first_departure_time: # an arrival
                next_event_time = next_arrival_time
                next_event_type = 1
            else:                                        # a departure
                next_event_time = first_departure_time
                next_event_type = 0

        # setup finished, turn to busy
        elif first_setup_finish_time < first_departure_time and first_setup_finish_time < first_countdown_to_turnoff_time:
            if next_arrival_time < first_setup_finish_time:  # an arrival
                next_event_time = next_arrival_time
                next_event_type = 1
            else:                                            # set up finished
                next_event_time = first_setup_finish_time
                next_event_type = 2

        elif first_countdown_to_turnoff_time < first_departure_time and first_countdown_to_turnoff_time < first_setup_finish_time:
            if next_arrival_time < first_countdown_to_turnoff_time:
                next_event_time = next_arrival_time
                next_event_type = 1
            else:
                next_event_time = first_countdown_to_turnoff_time
                next_event_type = 3
            

        master_clock = next_event_time


        if next_event_type == 1: # An arrival

            #
            # at least a server in the delayedoff state
            #
            if any(i == 3 for i in server_state):
                candidate_list = np.where(server_state == 3)[0]
                maxCountTimer = -1
                chosen_server = -1
                
                for serverID in candidate_list:
                    if maxCountTimer < delayedoff_timer_for_server[serverID]:
                        maxCountTimer = delayedoff_timer_for_server[serverID]
                        chosen_server = serverID

                next_departure_time[chosen_server] = next_arrival_time + service_time_next_arrival
                arrival_time_next_departure[chosen_server] = next_arrival_time
                server_state[chosen_server] = 2
            #
            # at least a server in the off state, then set up the server
            #
            elif any(i == 0 for i in server_state):
                candidate_list = np.where(server_state == 0)[0]
                chosen_server = np.min(candidate_list)
                server_state[chosen_server] = 1  # 1: SETUP
                set_up_time_for_server[chosen_server] = master_clock + setup_time
                buffer_content.append([next_arrival_time, service_time_next_arrival, 'marked'])
                queue_length += 1
            
            #
            # all servers are either in busy or setup
            #
            else:
                buffer_content.append([next_arrival_time, service_time_next_arrival, 'unmarked'])
                queue_length += 1


            next_arrival_time = master_clock - log(1 - random.random()) / lam
            service_time_next_arrival = -log(1 - random.random()) / mu + (-log(1 - random.random()) / mu) + (-log(1 - random.random()) / mu)

        elif next_event_type == 0: # A departure
            response_time_cumulative = response_time_cumulative + master_clock - arrival_time_next_departure[first_departure_server]
            num_customer_served += 1

            tmp = arrival_time_next_departure[first_departure_server]
            departure_info.append([tmp[0], master_clock])
            response_time_record.append(master_clock - tmp[0])

            if queue_length:
                to_be_processed = buffer_content[0]
                if to_be_processed[2] == 'unmarked':
                    next_departure_time[first_departure_server] = master_clock + to_be_processed[1]
                    arrival_time_next_departure[first_departure_server] = to_be_processed[0]
                    buffer_content.pop(0)
                    queue_length -= 1

                else:
                    found_unmarked = False
                    
                    for wait_index in range(1, len(buffer_content)):
                        if buffer_content[wait_index][2] == 'marked':
                            continue
                        found_unmarked = True
                        buffer_content[wait_index][2] = 'marked'
                        break

                    if found_unmarked == True: # there is at least a unmarked job
                        next_departure_time[first_departure_server] = master_clock + to_be_processed[1]
                        arrival_time_next_departure[first_departure_server] = to_be_processed[0]
                        buffer_content.pop(0)
                        queue_length -= 1
                        
                    else: # No unmarked job, needs to turn off a server
                        candidate_list = np.where(server_state == 1)[0]

                        chosen_server = -1
                        longestRemaining = -1
                        
                        for sID in candidate_list:
                            if set_up_time_for_server[sID] == Inf:
                                continue
                            if longestRemaining < set_up_time_for_server[sID]:
                                longestRemaining = set_up_time_for_server[sID]
                                chosen_server = sID

                        server_state[chosen_server] = 0
                        set_up_time_for_server[chosen_server] = Inf
                        next_departure_time[first_departure_server] = master_clock + to_be_processed[1]
                        arrival_time_next_departure[first_departure_server] = to_be_processed[0]
                        buffer_content.pop(0)
                        queue_length -= 1
                        
                        

            else:
                next_departure_time[first_departure_server] = Inf
                server_state[first_departure_server] = 3
                delayedoff_timer_for_server[first_departure_server] = master_clock + delayedoff_time

        elif next_event_type == 2: # setup finished, take a marked job from queue, state from setup to busy
            server_state[first_setup_finish_server] = 3
            set_up_time_for_server[first_setup_finish_server] = Inf
            to_be_processed = buffer_content[0]
            next_departure_time[first_setup_finish_server] = master_clock + to_be_processed[1]
            arrival_time_next_departure[first_setup_finish_server] = to_be_processed[0]
            buffer_content.pop(0)
            queue_length -= 1

        elif next_event_type == 3:
            server_state[first_countdown_to_turnoff_server] = 0
            delayedoff_timer_for_server[first_countdown_to_turnoff_server] = Inf


 
##    for i in departure_info:
##        print(i)
    #print(len(response_time_record))
    #print(response_time_record)
    #print(f'num_customer_served: {num_customer_served}')
    print(f'The estimated mean response time is: {response_time_cumulative/num_customer_served}')


##print(f'Tc time: {0.1}')
##random_mode(0.35, 1, 5, 5, 0.1, 16000)
##
##for i in range(1, 100):
##    print(f'Tc itme: {i}')
##    random_mode(0.35, 1, 5, 5, i, 16000)
##
##                
##
for i in range(1, 500, 10):
    print(i)
    random_mode(0.35, 1, 5, 5, i, 56000)                  
                    
                
                
                
            
            
        

    
