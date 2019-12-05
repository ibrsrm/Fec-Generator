class Buffer:
    def __init__(self, buffer, sequence, timestamp):
        self.__buffer = buffer
        self.__sequence = sequence
        self.__timestamp = timestamp

    def getBufferLength(self) :
        return len(self.__buffer)      

    def getBuffer(self) :
        return self.__buffer    

    def getTimestamp(self) :
        return self.__timestamp 
        
    def getSequence(self) :
        return self.__sequence 
