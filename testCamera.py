#!/usr/bin/python2
import time
import sys

class testCamera:
    def __init__(self):
        self.chipcount = 1
        self.test_par = "test_par"    #a test parameter
        self.dac={}
        print "testCamera init"
        
    def set_dac(self, thr, val, chip_id):
        self.dac[thr] = val
        #print self.dac
        
    def acquire(self, leng):
        time.sleep(leng)
        print "acquire"
        
    def _get_frame(self, i):
        time.sleep(i)
        print "get_frame {}".format(i)
        
    def build_frame(self):
        time.sleep(1)
        print "build_frame"
        return 0

if __name__ == "__main__":
    cam = testCamera()
    cam.set_dac("Thresh1", 70)
    cam.acquire(2)
    sys.exit(0)
