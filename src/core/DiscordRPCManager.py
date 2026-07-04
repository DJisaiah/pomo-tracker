from __future__ import annotations

import asyncio
import os
import time
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from pypresence import AioPresence  # type: ignore

if TYPE_CHECKING:
    from core.TimerPageUtils import TimerRPCPayload


load_dotenv()


class DiscordRPCManager:
    def __init__(self):
        self._client_id = os.getenv("DISCORD_CLIENT_ID", "1448550878255513710")
        self._state: str = "A great study sesh is on the way"
        self._details: str = "Opening books"
        self._name: str = "Pomo-Tracker"
        self._end_epoch: int | None = None
        self._start_epoch: int | None = None
        self._current_subject: str = "Nothing"

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
                        {
                            "label": "Try Pomo-Tracker",
                            "url": "https://github.com/DJisaiah/pomo-tracker/",
                        }
                    ],
                )
            await asyncio.sleep(15)
        except Exception as _:
            pass

    def update_details(self, new_state: str) -> None:
        self._details = new_state

    def update_state(
        self,
        new_state: str,
        end_epoch: int | None = None,
        start_epoch: int | None = None,
    ) -> None:
        self._state = new_state
        if end_epoch:
            self._end_epoch = end_epoch
        else:
            self._end_epoch = None
        if start_epoch:
            self._start_epoch = start_epoch
        else:
            self._start_epoch = None

    def timer_state_listener(self, payload: TimerRPCPayload) -> None:
        if payload.productive:
            if payload.running:
                if payload.paused:
                    self.update_details("Timer paused")
                    self.update_state(
                        f"was {payload.subject_type} {payload.subject_name}"
                    )
                elif payload.stopwatch:
                    self.update_details("Stopwatch Mode")
                    self.update_state(payload.current_time)
                elif payload.ended:
                    self.update_details("Timer finished!")
                    self.update_state(
                        f"another sesh of {payload.subject_name} in the bag"
                    )
                else:
                    self.update_details(
                        f"{payload.subject_type} {payload.subject_name}"
                    )
                    self.update_state(
                        payload.subject_type,
                        int(time.time() + payload.current_time_seconds),
                    )
        else:
            if payload.running:
                if payload.paused:
                    self.update_details("Timer paused")
                    self.update_state("taking a break...from a break?")
                elif payload.stopwatch:
                    self.update_details("How long I can take a break for?")
                    self.update_state(payload.current_time)
                elif payload.ended:
                    self.update_details("Timer finished!")
                    self.update_state(
                        f"Rested up from {payload.subject_name}. Back to business..."
                    )
                else:
                    self.update_details(f"Taking a break from {payload.subject_name}")
                    self.update_state(
                        "Do people read this?",
                        int(time.time() + payload.current_time_seconds),
                    )
