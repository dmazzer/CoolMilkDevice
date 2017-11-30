import time
import grovepi
import Queue
from threading import Thread

class Sensors():
    def __init__(self, sensor_lm35=14, q=None):
    
        self.sensor_lm35 = sensor_lm35
        self.q = q

        grovepi.pinMode(self.sensor_lm35,"INPUT")

        t = Thread(target=self.read_lm35, name='Buttons', args=(self.q, ))
        t.daemon = True
        t.start()    
    
    def read_lm35(self, q):
        while True:
            try:
                sensor_value = float(grovepi.analogRead(self.sensor_lm35))
                sensor_value = ((100.0 * sensor_value)/1024.0) * 5.0
                q.put(sensor_value)
                # print ("sensor_value = %.2f" %(sensor_value))
                time.sleep(0.2)

            except IOError:
                print ("Error")
