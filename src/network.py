 #!/usr/bin/python

import socket
import util
import threading
from time import sleep
from options import Options

class Sender (threading.Thread):
   __TAG = "NETWORK:"

   def __init__(self, name, finishedCallback, address, port, buffers):
      threading.Thread.__init__(self)
      self.__lock = threading.Lock()
      self.__name = name
      self.__address = address
      self.__port = port
      self.__buffers = buffers
      self.__running = False
      self.__interface = self.__getDefaultInterface()
      self.__finishedCallback = finishedCallback
      print(f"{self.__TAG} Multicast Addr:", self.__address, " port:", self.__port, " interface:", self.__interface)

   def __getDefaultInterface(self):
      route = "/proc/net/route"
      with open(route) as f:
         for line in f.readlines():
            try:
               iface, dest, _, flags, _, _, _, _, _, _, _, =  line.strip().split()
               if dest != '00000000' or not int(flags, 16) & 2:
                  continue
               return iface
            except:
               continue 
      return None           

   def __sendMessage(self, message): 
      addrinfo = socket.getaddrinfo(self.__address, None)[0]
      s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
      if self.__interface != None :
         s.setsockopt(socket.SOL_SOCKET, 25, str.encode(self.__interface))
         s.sendto(message, (addrinfo[4][0], self.__port))

   def run(self):
      self.__lock.acquire()
      self.__running = True
      self.__lock.release()
      clock = util.getCurrentTimeMs()
      size = len(self.__buffers)
      index = 0;
      
      #print(f"({self.__name}:) Starting sending packets size:", size, " ", util.getCurretTime())
      #print(f"({self.__name}:) First Timestamp", self.__buffers[index].getTimestamp())
      while True :
         self.__lock.acquire()
         if (self.__running == False) or (index >= size) : 
            self.__lock.release()
            break   
         self.__lock.release()
         timestamp = self.__buffers[index].getTimestamp()
         currentRefTime = util.getCurrentTimeMs() - clock
         delay = 0
         if (timestamp > currentRefTime) :
            delay = timestamp - currentRefTime
            delay /= 1000
         sleep(delay)    
         self.__sendMessage(self.__buffers[index].getBuffer())
         index += 1   
      #print(f"{self.__name}: Finished ", util.getCurretTime())
      self.__finishedCallback()     

   def stop(self):   
      self.__lock.acquire()
      self.__running = False
      self.__lock.release()
