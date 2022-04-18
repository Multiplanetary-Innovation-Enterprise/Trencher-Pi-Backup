from pynput import keyboard
from Connections import *
import time
import queue
import threading

class KeyboardInput():
    __messageChannel = None
    __stop = None
    __queue = None
    __isRunning = False
    __keyReleased = True
    __writer = None
    # lastMessage = None
    def __init__(self, writer):
        self.__writer = writer
        #start keyboard listener
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()  # start to listen on a separate thread
        self.__stop = False
        self.__queue = queue.Queue()
        thread = threading.Thread(target=self.processMessages)
        thread.start()

    def on_press(self, key):
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
        if k in ['up', 'down', 'w', 's', 'space', 'esc']:  # keys of interest
            # self.keys.append(k)  # store it in global-like variable
            self.sendMessage(Message('m', k))
        if (k == 'delete'):
            self.sendMessage(Message('s', 'Shutdown'))
            time.sleep(0.3)
            self.__stop = True
            return False  # stop listener

    def acceptingInput(self):
        if (self.__stop):
            return False
        else:
            return True

    def isRunning(self) -> bool:
        return self.__isRunning

    def enqueue(self, message) -> None:
        self.__queue.put(message)

    def dequeue(self):
        return self.__queue.get()

    def processMessages(self) -> None:
        # self.__isRunning = True
        # lastMessage = None
        while self.acceptingInput():
            while not self.__queue.empty():
                message = self.dequeue()
                print(f"sending message: {message.contents()}")
                self.__writer.send(message)
                time.sleep(0.1)

        # self.__isRunning = False

    def sendMessage(self, message):
        #Checks if the current command is the same as the last command
        # if not self.__isRunning:
        self.enqueue(message)
    #
    # def toggleLight(self, event):
    #     print("Toggle light")
    #     message = Message(MessageType.ACTION, Action.TOGGLE_LIGHTS)
    #     self.sendMessage(message, self.__messageChannel)
    #
    # def increaseBrightness(self, event):
    #     message = Message(MessageType.ACTION, Action.BRIGHTNESS_INCREASE)
    #     self.sendMessage(message, self.__messageChannel)
    #
    # def decreaseBrightness(self, event):
    #     message = Message(MessageType.ACTION, Action.BRIGHTNESS_DECREASE)
    #     self.sendMessage(message, self.__messageChannel)
