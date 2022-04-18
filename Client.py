#|*****************************************************************************|
#| Trencher Keyboard controller Client
#| Author: Conor Porter
#| Last Modified: 04/12/2021
#|*****************************************************************************|

from pynput import keyboard
from Connections import *
import sys
from KeyboardInput import KeyboardInput


def ControlMotor(command):# check if the switch is on and button is not pressed. If so, accelerate motor to max speed
    #start recording clock for tracking RPM data
    message = Message('m', command)
    w.send(message)

host = sys.argv[1]
port = 3000

foundPort = False
while not foundPort:
    try:
        s = ServerConnection(host, port)
        w = SocketWriter(s)
        message = Message('init', 'hello')
        w.send(message)
        r = SocketReader(s)
        message = r.receive()
        if (message.type() == 'init' and message.contents() == 'hello'):
            foundPort = True
    except:
        port += 1

kb = KeyboardInput(w)

while (kb.acceptingInput()):
    message = r.receive()
    if (message != None):
        if (message.type() == 'r'):
            print(message.contents())
