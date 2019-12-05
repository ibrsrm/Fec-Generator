class Options:
	__TAG = "OPTIONS:"

	def __init__(self, path, address, port, duration, size, d, l):
		self.__path = path
		self.__address = address
		self.__port = port
		self.__duration = duration
		self.__size = size
		self.__d = d
		self.__l = l
		self.__printOptions()

	def __printOptions (self):
		print(self.__TAG)
		print("\tfile path: ", self.__path)
		print("\taddress:   ", self.__address)
		print("\tport:      ", self.__port)
		print("\tbitrate:   ", self.__duration)
		print("\tchunk size:", self.__size)
		print("\td value:   ", self.__d)
		print("\tl value:   ", self.__l)	

	def getPath(self) : 
		return self.__path

	def getAddress(self) : 
		return self.__address

	def getPort(self) : 
		return self.__port
	
	def getDuration(self) : 
		return self.__duration

	def getSize(self) : 
		return self.__size

	def getD(self) : 
		return self.__d

	def getL(self) : 
		return self.__l
