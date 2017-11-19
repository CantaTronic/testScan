
#from marsct import marssystem
#from marsct import marscamera
from time import sleep
from time import time
from datetime import datetime
import sys
import timeit

from testCamera import testCamera as marscamera
import testSystem as marssystem


def print_img(frame, filename):
    pass
  #f = open(filename, 'w')
  #for i in range(len(frame)):
    #for j in range(len(frame[i])):
      #f.write("%s " % frame[i][j])
    #f.write('\n')
  #f.close()
  
def print_log(fname):
    #tcheck out what we have in log after tests call
    with open(fname, "r") as f:
        for line in f:             
            print(line)
    f.close()
  
def getFrame(camera):
    for i in range(camera.chipcount):
        camera._get_frame(i)
        

if __name__ == "__main__":
    #set up the number of repetitions for timing (or exit)
    argv = sys.argv
    if len(argv) < 2:
        print "Not enough arguments. Exiting..."
        sys.exit(0)
    else:
        reps = int(argv[1])
    
    #################################################################
    #set up testing environment
    print " ==== INITIALIZE CAMERA ===="
    system = marssystem.MarsSystem()
    camera = system.getCamera()
    
    print " ==== SET MODE ===="
    thresholds = [50, 15, 27, 18, 30, 21, 33, 24]
    for i in range(camera.chipcount):
        thresholds[i] = 44+i*11
        print "threshold{} = {}".format(i, thresholds[i])
        for j in range(len(thresholds)):
            camera.set_dac("Threshold{}".format(j), thresholds[j], i)
    print " ==== CAMERA INITIALIZED ===="
    
    print " ==== WAIT FOR HV WARMUP ===="
    #while camera.hv_state != marscamera.HV_ON:
        #sleep(1)
    #end of set up
    ##################################################################
    
    #####################---TESTING---################################
    
    #exp = [10.0, 20.0, 50.0, 100.0, 200.0]  #the real numbers
    #exp = [1.0, 2.0, 5.0, 10.0]     #the toy numbers
    exp = [1.0, 2.0, 3.0]     #a short toy numbers
    f = open("ref_test.log", 'w')
    f.write("Average time for {} iterations :\n".format(reps))
    for i in range(len(exp)):
        #f.write("Exp = {}:\n".format(exp[i]))
        f.write("\tacquire with exp = {}: {}\n".format(exp[i], timeit.timeit("camera.acquire(exp[i])", setup="from __main__ import camera; from __main__ import exp; from __main__ import i",number=reps)/reps))
    f.write("\tbuild_frame: {}\n".format(timeit.timeit("camera.build_frame()", setup="from __main__ import camera",number=reps)/reps))
    f.write("\tget_frame: {}\n".format(timeit.timeit("test_scan.getFrame(camera)", setup="import test_scan; from __main__ import camera",number=reps)/reps))
    image = camera.build_frame()    #I suppose there is no matter about how image was obtained
    f.write("\tsave_frame: {}\n".format(timeit.timeit("test_scan.print_img(image, 'img/test_frame.txt')", setup="import test_scan; from __main__ import image",number=reps)/reps))
    
    f.close()
    
    #end of tests
    ##################################################################
    print " ==== FINALIZE ===="
    system.finalise()
    print " ==== FINISHED ===="
    print "\n===================\n"
    
    print " ==== TIMING RESULTS ===="
    print_log("ref_test.log")
    
    sys.exit(0)
