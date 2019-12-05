from os import fstat
from options import Options

class Parser:
    __TAG = "PARSER:"
    __MAX_FRAME = 1000000
    __frames = []

    def __init__(self, path, size) :
        print(f"{self.__TAG} file path:", path, " chunk size:", size)
        self.__path = path
        self.__size = size
        self.__parseFile()
    
    def __parseFile(self) :
        count = 0
        handle = open(self.__path,'rb')
        try:
            while (True):
                frame = bytearray(handle.read(self.__size))
                if (frame[0] != 0x47):
                    print(f"{self.__TAG} sync byte cannot be found")
                    break   
                self.__frames.append(frame)
                count += 1; 
                if (count > self.__MAX_FRAME):
                    print(f"{self.__TAG} max frame reached")
                    break   
        except Exception as exception:
            if handle.tell() == fstat(handle.fileno()).st_size :
                print(f"{self.__TAG} end of file reached")
            else :
                print(f"{self.__TAG} io error occured")
        finally:
            handle.close()
            print(f"{self.__TAG} total frames found:", len(self.__frames))    
    
    def getFrames(self) : 
        return self.__frames
