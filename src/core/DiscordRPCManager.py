from __future__ import annotations
from pypresence import AioPresence
import time
import asyncio
#from dotenv import load_dotenv
import os

#load_dotenv()

class RPCManager:
    def __init__(self):
        self._client_id = os.getenv("DISCORD_CLIENT_ID", "1448550878255513710")
        self._state: str = "A great study sesh is on the way"
        self._details: str = "Opening books"
        self._name: str = "Pomo-Tracker"
        self._end_epoch: int = None
        self._start_epoch: int = None

    async def start_RPC(self) -> None:
        try:
            self._RPC = AioPresence(self._client_id)
            await self._RPC.connect()
            while True:
                await self._RPC.update(
                    state=self._state,
                    details=self._details,
                    name=self._name,
                    end=self._end_epoch,
                    large_image="icon",
                    buttons=[
                        {"label":"Try Pomo-Tracker", "url": "https://github.com/DJisaiah/pomo-tracker/"}
                    ]
                )
            await asyncio.sleep(15)
        except Exception as e:
            pass

    def update_details(self, new_state: str) -> None:
        self._details = new_state

    def update_state(self, new_state: str, end_epoch: int = None, start_epoch: int = None) -> None:
        self._state = new_state
        if end_epoch:
            self._end_epoch = end_epoch
        else:
            self._end_epoch = None
        if start_epoch:
            self._start_epoch = start_epoch
        else:
            self._start_epoch = None
