from __future__ import annotations

from typing import AsyncIterable

from fastapi_poe import PoeBot
from fastapi_poe.types import PartialResponse, QueryRequest, SettingsRequest, SettingsResponse


class BotFactory(PoeBot):
    async def get_response(
            self, request: QueryRequest
    ) -> AsyncIterable[PartialResponse]:
        last_message = request.query[-1].content
        create_args = parse_args(last_message)
        yield PartialResponse(text="# Bot description:\n")
        description = ""
        async for msg in generate_description(create_args):
            description += msg
            yield PartialResponse(text=msg)
        yield PartialResponse(text="\n# First message:\n")
        first_message = ""
        async for msg in generate_first_message(create_args, description):
            first_message += msg
            yield PartialResponse(text=msg)
        yield PartialResponse(text="\n# Example conversation:\n")
        async for msg in generate_conversation(create_args, description, first_message):
            yield PartialResponse(text=msg)

    async def get_settings(self, setting: SettingsRequest) -> SettingsResponse:
        return SettingsResponse(
            introduction_message="Hello! I'm your friendly bot. Start chatting with me."
        )


async def generate_description(create_args):
    for msg in ["This", " is", " test"]:
        yield msg


async def generate_first_message(create_args, description):
    for msg in ["This", " is", " test"]:
        yield msg


async def generate_conversation(create_args, description, first_message):
    for msg in ["This", " is", " test"]:
        yield msg


def parse_args(content):
    command_parts = content.strip().split(" ", 1)[1]
    seed_args = dict(part.split(":") for part in command_parts.split(";"))
    seed_args['categories'] = seed_args['categories'].split(",")
    seed_args['personalities'] = seed_args['personalities'].split(",")
    return seed_args
