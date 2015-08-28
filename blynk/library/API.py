import asyncio
from asyncio import async, sleep

from blynk.library.proto import BlynkProto, MsgType

@asyncio.coroutine
def pinger(blynk, interval):
	while True:
		yield from sleep(interval)
		blynk.protocol.format_send(MsgType.PING)


class Blynk(object):

	def __init__(self, auth, evloop=None):
		self.auth = auth
		self.evloop = evloop or asyncio.get_event_loop()

		self.evloop.set_debug(True)

	def connect(self, host="cloud.blynk.cc", port=8442, ssl=None):
		async( self.evloop.create_connection(lambda: BlynkProto(self.auth), host, port) ) \
			.add_done_callback(self._connected)
		return self

	def disconnect(self):
		pass #-- TODO

	def run_forever(self):
		try:
			self.evloop.run_forever()
		finally:
			self.evloop.close()

	def process_pending(self):
		pass #-- TODO

	def _connected(self, ft):
		transport, protocol = ft.result()
		self.protocol = protocol
		self.transport = transport

		async(pinger(self, 5))

