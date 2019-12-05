#!/usr/bin/python

import click
import threading
import util

from parser import Parser
from options import Options
from network import Sender
from fec_header import FecHeader
from rtp_stream import RtpStream
from fec_stream import FecStream

class Worker (threading.Thread):
    __TAG = "WORKER:"

    def __init__(self, address, port, rtpBuffers, fecBuffers):
        threading.Thread.__init__(self)
        self.__running = False
        self.__fecRunning = False
        self.__rtpRunning = False
        self.__address = address
        self.__port = port
        self.__condition = threading.Condition()
        self.__rtpBuffers = rtpBuffers
        self.__fecBuffers = fecBuffers
        self.__rtpSender = Sender("RTP Worker", self.__rtpFinishedCallback, self.__address, self.__port, self.__rtpBuffers)
        self.__fecSender = Sender("FEC Worker", self.__fecFinishedCallback, self.__address, self.__port + 2, self.__fecBuffers)    
        
    def __rtpFinishedCallback(self) :
        self.__condition.acquire()
        self.__rtpRunning = False
        self.__condition.notify()
        self.__condition.release()   

    def __fecFinishedCallback(self) :
        self.__condition.acquire()
        self.__fecRunning = False
        self.__condition.notify()   
        self.__condition.release()   
    
    def run(self):  
        self.__condition.acquire()
        self.__running = True
        self.__fecRunning = True
        self.__rtpRunning = True  
        self.__condition.release()

        self.__rtpSender.start()
        self.__fecSender.start()

        self.__condition.acquire()
        while (self.__running == True) and (self.__fecRunning == True or self.__rtpRunning == True) : 
            self.__condition.wait()  
        if self.__rtpRunning == True :
            self.__rtpSender.stop()
        if self.__fecRunning == True :    
            self.__fecSender.stop()    
        self.__condition.release()

        self.__rtpSender.join()
        self.__fecSender.join()
        print("Network packet sent finished")    

    def stop(self):     
        self.__condition.acquire()
        self.__running = False
        self.__condition.notify()
        self.__condition.release()   

@click.command()
@click.argument('filepath')
@click.argument('address')
@click.argument('port')
@click.argument('duration')
@click.argument('packetsize')
@click.argument('d')
@click.argument('l')
def main(filepath, address, port, duration, packetsize, d, l):
    """
    A tool o generate fec packets from a ts packet and 
    serve it on multicast network
    """

    print("Create Options, time", util.getCurretTime())
    opt = Options(filepath, address, int(port), int(duration), int(packetsize), int(d), int(l))
    print("")

    # Parse file, find chunks
    print("Create Parser, time", util.getCurretTime())
    prs = Parser(opt.getPath(), opt.getSize())
    print("")

    # Build rtp stream
    print("Create Rtp Stream, time", util.getCurretTime())
    rtpStream = RtpStream(prs.getFrames(), opt.getDuration())
    print("")
    
    # Build fec stream
    print("Create Fec Stream, time", util.getCurretTime())
    fecStream = FecStream(rtpStream.getBuffers(), opt.getD(), opt.getL())
    print("")

    print("Finished Setup, starting multicast, time", util.getCurretTime(), "\n")

    worker = Worker(address, int(port), rtpStream.getBuffers(), fecStream.getBuffers())
    worker.start()

    input("\nPress Enter to exit:\n") 
    worker.stop()   
    worker.join()    

if __name__ == "__main__":
    main()
