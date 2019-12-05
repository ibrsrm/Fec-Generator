from struct import pack

class FecHeader :
    __TAG = "FEC HEADER:"
    # TODO: change this according to needs
    # D     : "0" for fec packets computed on colums and "1" for on rows
    # Type  : "0" for XOR correction, "1" for Haming and "2" for Reed-Solomon
    # Offset: "L" for column correction "1" otherwise
    # NA    : "D" for column correction "L" for row correction
    __length_recovery = 0
    __e               = 0
    __pt_recovery     = 0
    __mask            = 0
    __ts_recovery     = 0
    __x               = 0
    __typ             = 0
    __index           = 0
    __sn_base_ext     = 0

    def __init__(self, snLow, correctionType, dValue, lValue) :
        self.__snLow = snLow
        if correctionType == 'column' :
            self.__d = 0
            self.__offset = lValue
            self.__na = dValue
        else :
            self.__d = 1
            self.__offset = 1
            self.__na = lValue
        self.__header = bytearray(0)
        self.__createHeader()

    def __createHeader(self) :
        self.__header.extend(pack('>H', self.__snLow))
        self.__header.extend(pack('>H', self.__length_recovery))
        number = (self.__e << 31) | (self.__pt_recovery << 24) | (self.__mask)
        self.__header.extend(pack('>I', number))
        self.__header.extend(pack('>I', self.__ts_recovery))
        number = (self.__x << 15) | (self.__d << 14) | (self.__typ << 11) | (self.__index << 8) | self.__offset
        self.__header.extend(pack('>H', number))
        number = (self.__na << 8) | (self.__sn_base_ext)
        self.__header.extend(pack('>H', number))

    def getHeader (self) :
        return self.__header        
