
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
  f = open(filename, 'w')
  for i in range(len(frame)):
    for j in range(len(frame[i])):
      f.write("%s " % frame[i][j])
    f.write('\n')
  f.close()
  
def test_args(arr):
  #print out the ginev array and exit
  for i in range(len(arr)):
    print "ar[{}] = {}".format(i,arr[i])
  print "len(argv) = {}".format(len(arr))
  sys.exit(0)
  
def test_acquire(exp_k, _reps):
    camera = testCamera()
    print " ==== TAKE SHOTS ===="
    for j in range(0, _reps):
        print "\033[K", j, "\r", #a simple decoration to watching the shot number
        sys.stdout.flush()
        camera.acquire(exp_k)
    print "DONE"
    sys.exit(0)
    

def test_main (argv=None):
    if argv is None:
        argv = sys.argv
      
    if len(argv) < 3:
        print "Not enough arguments. Exiting..."
        sys.exit(0)
    else:
        #set up main test parameters
        reps = int(argv[2])
        mode = argv[1]
      
        #test set up  ToDo: add normal unit tests, if it tends to become so serious...:)
        #print "mode = {}, reps = {}".format(mode,reps)
        #sys.exit(0)
      
        #run test
        print " ==== INITIALIZE CAMERA ===="
        system = marssystem.MarsSystem()
        camera = system.getCamera()
        print " ==== SET MODE ===="
        thresholds = [50, 15, 27, 18, 30, 21, 33, 24]
        for i in range(camera.chipcount):
            thresholds[i] = 44+i*11
            print "threshold{} = {}".format(i, thresholds[i])
            #thresholds[0] = 70
            for j in range(len(thresholds)):
                camera.set_dac("Threshold{}".format(j), thresholds[j], i)
                #camera.camera_driver[i].write_DACs({"Threshold{}".format(j): thresholds[j]})
        print " ==== CAMERA INITIALIZED ===="
        print " ==== WAIT FOR HV WARMUP ===="
        while camera.hv_state != marscamera.HV_ON:
            sleep(1)
        
        exp = [10.0, 20.0, 50.0, 100.0, 200.0]
        #reps = [10, 20, 40, 60, 100]
        
        #ceate a new log file marked by current datetime 
        curdate = datetime.strftime(datetime.now(), "%Y%m%d-%H%M")
        f = open("log/test_{}.log".format(curdate), 'w')
        
        #for p in range (len(reps)):
        for k in range (len(exp)):
            #start of bench
            start = time()
            
            f.write("Iter {}, {}:\n".format(reps,mode))
            for j in range(0, reps):
                print " ==== TAKE SHOTS ===="
                camera.acquire(exp[k])
                print " ==== GET IMAGES ===="
                if (mode == "build_frame"):
                    camera.build_frame()
                    #print_img(camera.build_frame(), "img_test/frame_all_{}_{}.txt".format(exp,j))
                elif (mode == "get_frame"):
                    for i in range(camera.chipcount):
                        camera._get_frame(i)
                        #print_img(camera._get_frame(i), "img/frame_{}_{}_{}.txt".format(exp,j,i))
                else:
                    print "Unknown mode. Exiting... "
                    sys.exit(0)

                  

            
            end = time()
            av = (end - start)/reps
            print "Average time is :"
            print av
            
            #f = open("test_iter011117.log", 'a')
            f.write("Exp = {}: average time is : {} \n".format(exp[k],av))

        f.close()
        print " ==== FINALIZE ===="
        system.finalise()
        print " ==== FINISHED ===="


if __name__ == "__main__":
    
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
    reps = 3
    f = open("ref_test.log", 'w')
    f.write("Iter {}:\n".format(reps))
    for i in range(len(exp)):
        f.write("Exp = {}: average time is : {} \n".format(exp[i], timeit.timeit("camera.acquire(exp[i])", setup="from __main__ import camera; from __main__ import exp; from __main__ import i",number=reps)/reps))
    f.close()
    print " ==== FINALIZE ===="
    system.finalise()
    print " ==== FINISHED ===="
