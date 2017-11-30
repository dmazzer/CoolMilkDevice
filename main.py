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

import time
sys.path.append('./')

from publisher import Publisher
from buttons import Buttons
from motors import Motors

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


logger = Logger('debug')

if __name__ == '__main__':
    
    logger.log("CoolMilk started", 'info')

    logger.log("publishing...")
    
    pub = Publisher()
    pub.publishData({'temp': 36, 'threshold': 37})

    button_queue = Queue.Queue()
    buttons = Buttons(q=button_queue)

    motors_queue = Queue.Queue()
    motors = Motors(q=motors_queue)
    
    print('comecou')
    motors_queue.put("start_mix")
    time.sleep(1)
    motors_queue.put("stop_mix")
    time.sleep(1)
    print('teminou')

    print("queues")
    while True:
        item = button_queue.get()
        print("item: " + str(item))
        if item:
            motors_queue.put("start_mix")
            
        button_queue.task_done()



    logger.log("done...")

    # Hold forever
    def do_exit(sig, stack):
        raise SystemExit('Exiting')
     
    signal.signal(signal.SIGINT, do_exit)
    signal.signal(signal.SIGUSR1, do_exit)
     
    signal.pause()





