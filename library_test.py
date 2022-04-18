import traceback
from Peripherals import *
from Connections import *

try:
    m = Motor(None, None, None, None)
except:
    traceback.print_exc()
    print('')

try:
    m = HallEffectSensor(None, None, None)
except:
    traceback.print_exc()
    print('')

try:
    m = CurrentSensor(None)
except:
    traceback.print_exc()
    print('')

try:
    m = ClientConnection(None)
except:
    traceback.print_exc()
    print('')

try:
    m = ServerConnection(None)
except:
    traceback.print_exc()
    print('')

try:
    m = SocketConnection()
except:
    traceback.print_exc()
    print('')

try:
    m = SocketReader(None)
except:
    traceback.print_exc()
    print('')

try:
    m = SocketWriter(None)
except:
    traceback.print_exc()
    print('')
