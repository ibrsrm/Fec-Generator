from struct import pack

class RtpHeader :
    __TAG = "RTP HEADER:"
    __version       = 2
    __p             = 0
    __x             = 0
    __cc            = 0
    __m             = 0
    __payload_type  = 0
    __ssrc          = 0

    def __init__(self, sequence, timestamp) :
        self.__sequence = sequence
        self.__timestamp = timestamp
        self.__header = bytearray(0)
        self.__createHeader()

    def __createHeader(self) :
        number = (self.__version << 6) | (self.__p << 5) | (self.__x << 4) | (self.__cc)
        number = (number << 8) | (self.__m << 7) | (self.__payload_type)
        self.__header.extend(pack('>H', number))
        self.__header.extend(pack('>H', self.__sequence))
        self.__header.extend(pack('>I', self.__timestamp))
        self.__header.extend(pack('>I', self.__ssrc))    

    def getHeader(self) :
        return self.__header        
    