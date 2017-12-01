#!/usr/bin/env python2

""" 
coolmilk.py: Cool Milk project
"""

__author__ = "Daniel Mazzer, Gilson Massayoshi Nakano, Alison Rafael"
__copyright__ = "Copyright 2017"
__credits__ = "Inatel"
__license__ = "MIT"
__maintainer__ = "Daniel Mazzer"
__email__ = "daniel.mazzer@inatel.br"


import logging
import signal
from uuid import uuid1
import sys
import Queue
from threading import Thread
import numpy as np

import time
sys.path.append('./')

from publisher import Publisher
from buttons import Buttons
from motors import Motors
from sensors import Sensors

class Logger():
    def __init__(self, level='info'):
        
        levels =  {
                    'debug':logging.DEBUG,
                    'info':logging.INFO,
                    'critical':logging.CRITICAL,
                    'error':logging.ERROR,
                    'fatal':logging.FATAL,
                    'warning':logging.WARNING,
                   }
  
        setlevel = levels.get(level, logging.NOTSET)
        
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=setlevel,
                        format='[%(asctime)s %(threadName)s] %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S')
    
    def log(self, msg, level='info'):
        levelsfun =  {
                    'debug':self.logger.debug,
                    'info':self.logger.info,
                    'critical':self.logger.critical,
                    'error':self.logger.error,
                    'fatal':self.logger.fatal,
                    'warning':self.logger.warning,
                   }
        self.setlevelfun = levelsfun.get(level, self.logger.info)
        self.setlevelfun(msg)


logger = Logger('info')

if __name__ == '__main__':
    
    logger.log("CoolMilk started", 'info')

    pub = Publisher()

    button_queue = Queue.Queue()
    buttons = Buttons(q=button_queue)

    motors_queue = Queue.Queue()
    motors = Motors(q=motors_queue)
    
    sensors_queue = Queue.Queue()
    sensors = Sensors(q=sensors_queue)

    process_start_stop_status = 'stop'
    process_mixer_status = 'stop'
    process_cooling_status = 'stop'
    process_start_time = 0
    pricess_mixing_start_time = 0


    # process parameters

    time_milking = 60
    time_milking_message = 0

    time_mixing_stop = 10
    time_mixing_runnig = 4

    temp_min = 14.0
    temp_max = 18.0
    temp_max_milking = 30.0

    temp = temp_max


    while True:
        if button_queue.empty() == False:
            item = button_queue.get()
            if item == 1:
                if process_start_stop_status == 'start': 
                    process_start_stop_status = 'stop' 
                    process_cooling_status = 'stop'
                    process_mixer_status = 'stop'
                    motors_queue.put('stop_cool')
                    motors_queue.put('stop_mix')
                else:
                    process_start_stop_status = 'start'
                    process_mixer_status = 'running_start'
                    process_cooling_status = 'start'
                    time_milking_message = 0
                    process_start_time = int(time.time())
                    pricess_mixing_start_time = int(time.time())
                    motors_queue.put('start_mix')
                print('Processes start/stop: ' + process_start_stop_status)
            button_queue.task_done()
        
        if sensors_queue.empty() == False:
            temp_array = []
            while sensors_queue.empty() == False:
                temp_array.append(sensors_queue.get())
            temp_x = sum(temp_array) / float(len(temp_array)) 
            if temp_x < 30:
                temp = temp_x
            sensors_queue.queue.clear()
            # print('Temp: ' + str(temp))

        if process_start_stop_status == 'start':
            if int(time.time()) > (process_start_time + time_milking):
                if time_milking_message == 0:
                    time_milking_message = 1
                    print('Milking time endded')

            if temp >= temp_max:
                motors_queue.put('start_cool')
                process_cooling_status = 'start'
            if temp <= temp_min:
                motors_queue.put('stop_cool')
                process_cooling_status = 'stop'

            if process_mixer_status == 'running_start':
                if int(time.time()) > (pricess_mixing_start_time + time_mixing_runnig):
                    print('Mixer stop')
                    process_mixer_status = 'running_stop'
                    motors_queue.put('stop_mix')
                    pricess_mixing_start_time = int(time.time())

            if process_mixer_status == 'running_stop':
                if int(time.time()) > (pricess_mixing_start_time + time_mixing_stop):
                    print('Mixer start')
                    process_mixer_status = 'running_start'
                    motors_queue.put('start_mix')
                    pricess_mixing_start_time = int(time.time())
                    
        message = dict()
        if process_mixer_status == 'running_start':
            message['mixer'] = 1
        else:
            message['mixer'] = 0
        
        if process_start_stop_status == 'start':
            message['process'] = 1
        else:
            message['process'] = 0
        
        if process_cooling_status == 'start':
            message['cooler'] = 1
        else:
            message['cooler'] = 0
        
        message['temp'] = temp

        process_mask = ((temp_max - temp_max_milking)/float(time_milking)) * float(int(time.time()) - process_start_time) + temp_max_milking
        process_mask = min(process_mask, temp_max_milking)
        process_mask = max(process_mask, temp_max)
        message['mask'] = process_mask
        
        print(str(message))

        pub.publishData(message)




            
        time.sleep(1)



    print('comecou')
    motors_queue.put("start_mix")
    time.sleep(5)
    motors_queue.put("stop_mix")
    time.sleep(1)
    print('teminou')


    print('comecou')
    motors_queue.put("start_cool")
    time.sleep(10)
    motors_queue.put("stop_cool")
    time.sleep(1)
    print('teminou')



    print("queues")



    logger.log("done...")

    # Hold forever
    def do_exit(sig, stack):
        raise SystemExit('Exiting')
     
    signal.signal(signal.SIGINT, do_exit)
    signal.signal(signal.SIGUSR1, do_exit)
     
    signal.pause()





