from __future__ import annotations
from typing import AsyncIterable
from modal import Image, Stub, asgi_app
from fastapi_poe import PoeBot, make_app
from fastapi_poe.types import (
    PartialResponse,
    QueryRequest,
    SettingsRequest,
    SettingsResponse,
)

class BabyBot(PoeBot):
    async def get_response(self, query: QueryRequest) -> AsyncIterable[PartialResponse]:
        # The bot will always greet the user and ask how they're doing
        yield self.text_event("Hi, how are you doing?")

    async def get_settings(self, setting: SettingsRequest) -> SettingsResponse:
        return SettingsResponse(
            introduction_message="Hello! I'm your friendly bot. Start chatting with me."
        )