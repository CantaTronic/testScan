#!/usr/bin/python2
import time
import sys

class testCamera:
    def acquire(self,leng):
        time.sleep(leng)
        print "acquire"

if __name__ == "__main__":
    cam = testCamera()
    cam.acquire(2)
    sys.exit(0)
