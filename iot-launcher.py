# -*- coding: utf-8 -*-
import sys
import subprocess
import os
import shutil
import random
import signal
import time

spawns=[] #list of subprocesses spawned 

def usage():
    print "iot-launcher.py <server_ip> <server_port> <sim_time> <num_of_sensors>"

def signal_handler(signal, frame):
  print 'Shutting down Launcher...'
  #probably need to close all the forked subprocesses?
  sys.exit(0)

def main(argv):
  ipaddr="localhost"
  port="5000"
  sim_time=200 #seconds
  N=1 #or >4 (number of sensors)
  
  if(len(argv)>=2):
     ipaddr=argv[0]
     port=argv[1]
     if(len(argv)>=3):
      sim_time=int(argv[2])
      if(len(argv)==4):
        N=int(argv[3])
  if len(argv)!=0:
    if (argv[0] == "-h" or argv[0]=="--help"):
      usage()
      sys.exit(0)
  else:
    print "using Launcher defaults =>"

  print "ip",ipaddr,"and port:",port
  print "sim_time",sim_time
  print "number of sensors",N
  
  start_time = round(time.time(), 3)
  #[STEP1]: starting IoT Server to handle input from sensors
  spawns.append(subprocess.Popen(["python","iot-server.py", ipaddr, port],stdout=True,shell=False))

  #[STEP2]: starting sensors
  sensors=["device", "temp", "gps", "camera"]
  for i in range(N): 
    #choose randomly a sensor from the list
    sensor_type=sensors[i]
    sid=str(i)
    
    if (N>4):
      sensor_type=random.choice(sensors)
      sid=str(random.randint(10000,99999))
    
    print "starting",i,sensor_type,"...\n"
    #forking a subprocess 
    spawns.append(subprocess.Popen(["python","sensor.py", sensor_type, ipaddr, port, sid],stdout=False,shell=False))
    #print spawns[i].pid
    #spawns[i].wait()

  #[STEP3]: start your clients here
  #append processes to spawns list. so that we can kill them. Also implement Ctrl+C 


  time.sleep(sim_time)
  print "killing processes after", (time.time()-start_time)
  for s in spawns:
    #print s.pid
    os.kill(s.pid, signal.SIGINT)

if __name__ == "__main__":
  signal.signal(signal.SIGINT, signal_handler)
  main(sys.argv[1:])