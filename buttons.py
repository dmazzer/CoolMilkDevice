
import time
import grovepi
import Queue
from threading import Thread

class Buttons():
    def __init__(self, digital_port = 8, q=None):
        self.digital_port = digital_port
        self.q = q # queue

        grovepi.pinMode(self.digital_port,"INPUT")
        
        t = Thread(target=self.read_start_stop_switch, name='Buttons', args=(self.q, ))
        t.daemon = True
        t.start()    

    def read_start_stop_switch(self, q):

        while True:
            try:
                button = grovepi.digitalRead(self.digital_port)
                if button == 1:
                    # print("Button pressed!")
                    q.queue.clear()
                    q.put(1)
                
                time.sleep(1)

            except IOError:
                print ("Error")

