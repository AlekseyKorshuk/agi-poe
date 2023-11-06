from __future__ import annotations

import random
import time
from typing import AsyncIterable

from fastapi_poe import PoeBot
from fastapi_poe.client import stream_request
from fastapi_poe.types import PartialResponse, QueryRequest, SettingsRequest, SettingsResponse, ProtocolMessage

from config import TEXT_MODEL, IMAGE_MODEL
from generators.bio import generate_bio
from generators.greeting_message import generate_greeting_message
from generators.handle import generate_handle
from generators.image import generate_image
from generators.name import generate_name
from generators.prompt import generate_prompt
from utils import parse_args, GenerationState, get_full_response
from copy import deepcopy


class BotFactory(PoeBot):
    async def get_response(
            self, request: QueryRequest
    ) -> AsyncIterable[PartialResponse]:
        last_message = request.query[-1].content
        # create_args = parse_args(last_message)
        create_args = {}

        generation_state = GenerationState()
        async for msg in generate_name(deepcopy(request), create_args, generation_state):
            generation_state.name += msg

        yield PartialResponse(text="### Bot handle\n")
        async for msg in generate_handle(deepcopy(request), create_args, generation_state):
            generation_state.handle += msg
            yield PartialResponse(text=msg)

        yield PartialResponse(text="\n### Bio\n")
        async for msg in generate_bio(deepcopy(request), create_args, generation_state):
            generation_state.bio += msg
            yield PartialResponse(text=msg)

        yield PartialResponse(text="\n### Prompt\n")
        async for msg in generate_prompt(deepcopy(request), create_args, generation_state):
            generation_state.prompt += msg
            yield PartialResponse(text=msg)

        yield PartialResponse(text="\n### Greeting message\n")
        async for msg in generate_greeting_message(deepcopy(request), create_args, generation_state):
            generation_state.greeting_message += msg
            yield PartialResponse(text=msg)

        yield PartialResponse(
            text=get_full_response(generation_state),
            is_replace_response=True
        )

        async for msg in generate_image(deepcopy(request), create_args, generation_state):
            yield PartialResponse(text=msg)

    # async def get_settings(self, setting: SettingsRequest) -> SettingsResponse:
    #     return SettingsResponse(
    #         introduction_message="Hello! I'm your friendly bot. Start chatting with me.",
    #         server_bot_dependencies={"GPT-3.5-Turbo": 1}
    #     )

    async def get_settings(self, setting: SettingsRequest) -> SettingsResponse:
        return SettingsResponse(
            introduction_message=f"Welcome to PoeFactory! Tell me your bot idea, like \"plumber named Bill\", "
                                 "then watch it come to life.",
            server_bot_dependencies={
                TEXT_MODEL: 5,
                # "GPT-4": 1,
                IMAGE_MODEL: 1,
            }
        )
