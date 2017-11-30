import time
import grovepi
import Queue
from threading import Thread


class Motors():
    def __init__(self, cool=3, mix=4, q=None):
        self.cool = cool
        self.mix = mix
        self.q = q

        grovepi.pinMode(self.cool,"OUTPUT")
        grovepi.pinMode(self.mix,"OUTPUT")
        time.sleep(1)

        tcool = Thread(target=self.start_cooling, name='Motor cooling', args=(self.q, ))
        tcool.daemon = True
        tcool.start()    
        # tmix = Thread(target=self.start_mix, name='Motor mixer', args=(self.q, ))
        # tmix.daemon = True
        # tmix.start()    
        
    def start_cooling(self, q):
        while True:
            try:
                status = self.q.get()
                if status == "start_cool":
                    grovepi.digitalWrite(self.cool,1)
                    print ("Cool ON")

                if status == "stop_cool":
                    grovepi.digitalWrite(self.cool,0)
                    print ("Cool OFF")

                if status == "start_mix":
                    grovepi.digitalWrite(self.mix,1)
                    print ("Mix ON")

                if status == "stop_mix":
                    grovepi.digitalWrite(self.mix,0)
                    print ("Mix OFF")

            except IOError:				# Print "Error" if communication error encountered
                print ("Error")

    # def start_mix(self, q):


