
from marsct import marssystem
from marsct import marscamera
from time import sleep

def print_img(frame, filename):
  f = open(filename, 'w')
  for i in range(len(frame)):
    for j in range(len(frame[i])):
      f.write("%s " % frame[j][i])
    f.write('\n')
  f.close()

def main():
  print " ==== INITIALIZE CAMERA ===="
  system = marssystem.MarsSystem()
  camera = system.getCamera()
  print " ==== SET MODE ===="
  thresholds = [50, 15, 27, 18, 30, 21, 33, 24]
  for i in range(camera.chipcount):
    thresholds[0] = 44+i*11
    for j in range(len(thresholds)):
      camera.set_dac("Threshold{}".format(j), thresholds[j], i)
      #camera.camera_driver[i].write_DACs({"Threshold{}".format(j): thresholds[j]})
  print " ==== CAMERA INITIALIZED ===="
  print " ==== WAIT FOR HV WARMUP ===="
  while camera.hv_state != marscamera.HV_ON:
    sleep(1)
  print " ==== TAKE SHOTS ===="
  camera.acquire(100.0)
  print " ==== GET IMAGES ===="
  for i in range(camera.chipcount):
    print_img(camera._get_frame(i), "frame{}.txt".format(i))
  print " ==== FINALIZE ===="
  system.finalise()
  print " ==== FINISHED ===="

if __name__ == "__main__":
  main()
