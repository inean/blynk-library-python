from enum import Enum

from blynk.lib.board import Board

class MsgType(Enum):
    RSP    = 0
    LOGIN  = 2
    PING   = 6
    BRIDGE = 15
    HW     = 20


class MsgStatus(Enum):
    OK     = 200


#-- to be continued...
