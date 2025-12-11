from pypresence import AioPresence
import time
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

class RPCManager:
	def __init__(self):
		self._client_id = os.getenv("DISCORD_CLIENT_ID")
		self._state = "A great study sesh is on the way"
		self._details = "Opening books"
		self._name = "Pomo-Tracker"

	async def start_RPC(self):
		try:
			self._RPC = AioPresence(self._client_id)
			await self._RPC.connect()

			while True:
				await self._RPC.update(
					state=self._state,
					details=self._details,
					name=self._name,
					large_image="icon",
					buttons=[
						{"label":"Try Pomo-Tracker", "url": "https://github.com/DJisaiah/pomo-tracker/"}
					]
					)
				await asyncio.sleep(15)
		except Exception as e:
			pass

	def update_state(self, new_state):
		self._state = new_state

	def update_details(self, new_details):
		self._details = new_details
