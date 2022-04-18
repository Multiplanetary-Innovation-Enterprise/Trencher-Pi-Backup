from socket import *
import pickle
import time

class SocketConnection():
    __socket = None;

    def __init__(self, *args):
        if (len(args) == 0):
            self.__socket = socket(AF_INET, SOCK_STREAM)
        else:
            self.__socket = args[0]

    def get(self):
        return self.__socket

    def close(self):
        self.__socket.close();

    def setTimeout(self, seconds):
        self.__socket.settimeout(seconds)


class ServerConnection(SocketConnection):
    __host = None
    __port = None

    def __init__(self, host, port):
        super().__init__()
        self.__host = host
        self.__port = port
        super().setTimeout(1)
        self.get().connect((host, port))

    def getHost(self):
        return self.__host

    def getPort(self):
        return self.__port

class ClientConnection(SocketConnection):
    __port = None
    __clientSocket = None
    __clientAddress = None

    def __init__(self, port):
        super().__init__()
        self.__port = port
        self.get().bind(('', port))

    def getPort(self):
        return self.__port

    def client(self):
        return self.__clientSocket

    def claddr(self):
        return self.__clientAddress

    def listenAndAccept(self, seconds):
        self.get().listen(seconds)
        connection, address = self.get().accept()
        self.__clientSocket = SocketConnection(connection)
        self.__clientAddress = address

class SocketReader():
    __socket = None
    MAX_MSG = 8192

    def __init__(self, socket):
        self.__socket = socket.get()

    def getSocket(self):
        return self.__socket

    def decode(self, message):
        return pickle.loads(message)

    def receive(self):
        msg = self.__recv_timeout(self.__socket, 0.1)
        if (msg != None):
            return self.decode(msg)
        return msg

    def __recv_timeout(self, the_socket, timeout): #NOTE: may need to modify so it blocks for the first chunk
        #make socket non blocking
        the_socket.setblocking(0)

        #total data partwise in an array
        total_data=[];
        data='';

        #beginning time
        begin=time.time()
        while 1:
            #if you got some data, then break after timeout
            if total_data and time.time()-begin > timeout:
                break

            #if you got no data at all, wait a little longer, twice the timeout
            elif time.time()-begin > timeout*2:
                break

            #recv something
            try:
                data = the_socket.recv(self.MAX_MSG)
                if data:
                    total_data.append(data)
                    #change the beginning time for measurement
                    begin = time.time()
                # else:
                #     #sleep for sometime to indicate a gap
                #     time.sleep(0.1)
            except:
                pass

        if (len(total_data) > 0):
            #join all parts to make final string
            return b''.join(total_data)
        else:
            return None #NOTE: still errors, needs to be a byte-like object

class SocketWriter():
    __socket = None

    def __init__(self, socket):
        self.__socket = socket.get()

    def encode(self, message):
        return pickle.dumps(message)

    def send(self, message):
        self.__socket.send(self.encode(message))

class Message():
    __messageType = None
    __message = None

    def __init__(self, messageType, message):
        self.__messageType = messageType
        self.__message = message

    def type(self):
        return self.__messageType

    def contents(self):
        return self.__message
