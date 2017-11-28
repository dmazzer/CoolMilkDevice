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

import Publisher

logger = Logger('debug')


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


if __name__ == '__main__':
    
    logger.log("CoolMilk started", 'info')

    # Hold forever
    def do_exit(sig, stack):
        raise SystemExit('Exiting')
     
    signal.signal(signal.SIGINT, do_exit)
    signal.signal(signal.SIGUSR1, do_exit)
     
    signal.pause()





