from rtp_header import RtpHeader
from buffer import Buffer

class RtpStream:
    __TAG = "RTPSTREAM:"
    __chunkPerPacket = 7
    __MAX_SEQUENCE = 65536
    __buffers = []

    def __init__(self, frames, duration):
        print(f"{self.__TAG} frame count:", len(frames), " duration:", duration)
        self.__frames = frames
        self.__duration = duration
        self.__createBuffers()
        
    def __createBuffers(self) :
        size = len(self.__frames)
        size /= self.__chunkPerPacket
        size = int(size)
        durationMs = (self.__duration * 1000)
        durationMs /= size
        timestamp = 0
        sequence = 0
        for x in range(size) :
            rtpHeader = RtpHeader(sequence, 0)
            packet = bytearray()
            packet.extend(rtpHeader.getHeader())
            for y in range(self.__chunkPerPacket) :
                packet.extend(self.__frames[x * self.__chunkPerPacket + y])
            buffer = Buffer(packet, sequence, timestamp)    
            self.__buffers.append(buffer)
            sequence += 1
            sequence %= self.__MAX_SEQUENCE
            timestamp += durationMs

    def getBuffers(self) :
        return self.__buffers  
