from fec_header import FecHeader
from rtp_header import RtpHeader
from buffer import Buffer

class FecStream:
    __TAG = "FECSTREAM:"
    __MAX_SEQUENCE = 65536
    __buffers = []
    __startIndex = 12

    def __init__(self, frames, dValue, lValue):
        print(f"{self.__TAG} frame count:", len(frames), " D:", dValue, " L:", lValue)
        self.__frames = frames
        self.__d = dValue
        self.__l = lValue
        self.__createBuffers()
     
    def __createPayload(self, chunkList) :
        size = len(chunkList)
        length = chunkList[0].getBufferLength()
        payload = bytearray()
        for x in range(self.__startIndex, length) : 
            b = 0
            for y in range(size) :
                b ^= (chunkList[y].getBuffer())[x]
            payload.append(b)       
        return payload
            
    def __createBuffers(self) :
        size = len(self.__frames)
        index = 0
        sequence = 0
        while True :
            if (index + self.__l * self.__d) >= size :
                break
            timestamp_index = index    
            for x in range(self.__l) :
                list = []
                for y in range(self.__d) :
                    list.append(self.__frames[index + y * self.__l])
                rtpHeader = RtpHeader(sequence, 0)
                fecHeader = FecHeader(self.__frames[index].getSequence(), "column", self.__d, self.__l)
                packet = bytearray()
                packet.extend(rtpHeader.getHeader())
                packet.extend(fecHeader.getHeader())
                packet.extend(self.__createPayload(list)) 
                tmp = timestamp_index + self.__l * self.__d + x * self.__d
                if tmp >= size :
                    tmp = size - 1 
                timestamp = self.__frames[tmp].getTimestamp()        
                buffer = Buffer(packet, sequence, timestamp) 
                self.__buffers.append(buffer)
                index += 1
                sequence += 1
            index += (self.__l * (self.__d - 1))      

    def getBuffers(self) :
        return self.__buffers  
