from __future__ import annotations

import time
from typing import AsyncIterable

from fastapi_poe import PoeBot
from fastapi_poe.types import PartialResponse, QueryRequest, SettingsRequest, SettingsResponse

from generators.bio import generate_bio
from generators.greeting_message import generate_greeting_message
from generators.handle import generate_handle
from generators.prompt import generate_prompt
from utils import parse_args, GenerationState


class BotFactory(PoeBot):
    async def get_response(
            self, request: QueryRequest
    ) -> AsyncIterable[PartialResponse]:
        last_message = request.query[-1].content
        # create_args = parse_args(last_message)
        create_args = {}

        generation_state = GenerationState()
        yield PartialResponse(text="# Bot handle:\n")
        async for msg in generate_handle(request, create_args, generation_state):
            generation_state.handle += msg
            yield PartialResponse(text=msg)
        print(generation_state)

        yield PartialResponse(text="\n# Bot bio:\n")
        async for msg in generate_bio(request, create_args, generation_state):
            generation_state.bio += msg
            yield PartialResponse(text=msg)
        print(generation_state)

        yield PartialResponse(text="\n# Bot prompt:\n")
        async for msg in generate_prompt(request, create_args, generation_state):
            generation_state.prompt += msg
            yield PartialResponse(text=msg)
        print(generation_state)

        yield PartialResponse(text="\n# Greeting message:\n")
        async for msg in generate_greeting_message(request, create_args, generation_state):
            generation_state.greeting_message += msg
            yield PartialResponse(text=msg)
            print(generation_state)

    # async def get_settings(self, setting: SettingsRequest) -> SettingsResponse:
    #     return SettingsResponse(
    #         introduction_message="Hello! I'm your friendly bot. Start chatting with me.",
    #         server_bot_dependencies={"GPT-3.5-Turbo": 1}
    #     )

    async def get_settings(self, setting: SettingsRequest) -> SettingsResponse:
        return SettingsResponse(
            server_bot_dependencies={"GPT-4": 5}
        )
