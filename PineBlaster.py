#####################################################################
#                                                                   #
# /PineBlaster.py                                                   #
#                                                                   #
# Copyright 2013, Monash University                                 #
#                                                                   #
# This file is part of the module labscript_devices, in the         #
# labscript suite (see http://labscriptsuite.org), and is           #
# licensed under the Simplified BSD License. See the license.txt    #
# file in the root of the project for the full license.             #
#                                                                   #
#####################################################################

from labscript_devices import RunviewerParser

import numpy as np
import labscript_utils.h5_lock, h5py

    
@RunviewerParser
class RunviewerClass(object):
    clock_resolution = 25e-9
    clock_type = 'fast clock'
    # Todo: find out what this actually is:
    trigger_delay = 1e-6
    # Todo: find out what this actually is:
    wait_delay = 2.5e-6
    
    def __init__(self, path, name):
        self.path = path
        self.name = name
        
            
    def get_traces(self,clock=None):
        if clock is not None:
            times, clock_value = clock[0], clock[1]
            clock_indices = np.where((clock_value[1:]-clock_value[:-1])==1)[0]+1
            # If initial clock value is 1, then this counts as a rising edge (clock should be 0 before experiment)
            # but this is not picked up by the above code. So we insert it!
            if clock_value[0] == 1:
                clock_indices = np.insert(clock_indices, 0, 0)
            clock_ticks = times[clock_indices]

        
            
        # get the pulse program
        with h5py.File(self.path, 'r') as f:
            pulse_program = f['devices/%s/PULSE_PROGRAM'%self.name][:]
            
        time = []
        states = []
        trigger_index = 0
        t = 0 if clock is None else clock_ticks[trigger_index]+self.trigger_delay
        trigger_index += 1
        
        clock_factor = self.clock_resolution/2.
        
        for row in pulse_program:
            if row['period'] == 0:
                #special case
                if row['reps'] == 1: # WAIT
                    if clock is not None:
                        t = clock_ticks[trigger_index]+self.trigger_delay
                        trigger_index += 1
                    else:
                        t += self.wait_delay
            else:    
                for i in range(row['reps']):
                    for j in range(1, -1, -1):
                        time.append(t)
                        states.append(j)
                        t += row['period']*clock_factor
                        
        traces = {'fast clock':(np.array(time), np.array(states))}
        return traces
    