
import asyncio

from enum import Enum
from struct import Struct

import logging

from blynk.library.board import Board

#-- for from blynk.library.proto import *
__all__ = ['MsgType', 'MsgStatus', 'BlynkProto']


class MsgType(Enum):
    RESPONSE    = 0
    REGISTER    = 1
    LOGIN       = 2
    GET_TOKEN   = 5
    PING        = 6
    TWEET       = 12
    EMAIL       = 13
    NOTIFY      = 14
    BRIDGE      = 15
    HARDWARE    = 20


class MsgStatus(Enum):
    OK                 = 200
    QUOTA_LIMIT        = 1
    ILL_COMMAND        = 2
    NOT_REGISTERED     = 3
    ALREADY_REGISTERED = 4
    NO_AUTH            = 5
    NOT_ALLOWED        = 6
    NO_CONNECTION      = 7
    NO_DASHBOARD       = 8
    INVALID_TOKEN      = 9
    DEVICE_OFFLINE     = 10
    ALREADY_LOGGED_IN  = 11

    TIMEOUT            = 16

hdr = Struct("!BHH")


def format_send(bp, msgtype, *args):
    payload = bytes.join(b'\0', map(lambda a: str(a).encode('UTF-8'), args))
    pdu = hdr.pack(msgtype.value, bp.msgid, len(payload)) + payload
    bp.transport.write(pdu)
    return pdu


def msgid_gen():
    nid = 0xC0FE
    while True:
        yield nid
        nid = 1 if nid >= 0xFFFF else nid + 1


class BlynkProto(asyncio.Protocol):

    def __init__(self, authtoken):
        self.authtoken = authtoken
        self.buf = bytes(0)

    @property
    def msgid(self, g=msgid_gen()): #-- FIXME: it's a single per-class counter, not per-instance
        return next(g)

    def connection_made(self, transport):
        self.transport = transport
        self.format_send(MsgType.LOGIN, self.authtoken)

    def data_received(self, data):
        self.buf += data

        while len(self.buf) >= 5:
            #-- unpack message header
            msg_type, msg_id, stat_len = hdr.unpack_from(self.buf)
            bytes_consumed = 5

            #-- extract payload if present
            args = self.buf[5:5+stat_len].split(b'\0') if stat_len > 0 else ()
            bytes_consumed += stat_len

            #-- select and call appropriate handler
            handler = BlynkProto.handlers.get(msg_type, BlynkProto.handle_unknown_msgtype)
            bytes_consumed += handler(self, *args) or 0

            #-- trim buffer
            self.buf = self.buf[bytes_consumed:]

    format_send = format_send

    def handle_LOGIN(self):
        pass

    def handle_PING(self):
        pass

    def handle_GET_TOKEN(self):
        pass

    def handle_NOTIFY(self):
        pass

    def handle_BRIDGE(self):
        pass

    def handle_HARDWARE(self, *params):
        pass #-- TODO implement me

    def handle_unknown_msgtype(self, *params):
        logging.warn("received unknown msgtype %d; params=%r", self.buf[0], params)

    handlers = {
            #MsgType.LOGIN:     handle_LOGIN,
            #MsgType.RESPONSE:  handle_RESPONSE,
            #MsgType.GET_TOKEN: handle_GET_TOKEN,
            MsgType.HARDWARE: handle_HARDWARE,
            }

    #def __repr__(self):

