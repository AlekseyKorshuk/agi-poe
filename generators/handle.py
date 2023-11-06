from fastapi_poe.client import stream_request
from fastapi_poe.types import QueryRequest, ProtocolMessage

from config import TEXT_MODEL
from utils import GenerationState

system = """Your task is to rewrite character name to make is as username/handle. Each handle should be unique, but should not contain numbers. 

Handle rules:
Character handle that should be unique and use 4-20 characters, including letters, dashes and underscores.

Examples of good changes:
- ML Engineer -> ML-Engineer
- Jake Classmate -> Jake-Classmate
- Read My Mind -> Read-My-Mind or ReadMind
- Akinator -> Akinator or IAmAkinator
- Vampire Queen -> Vampire-Queen
- Mark Zuckerberg (CEO of Meta) -> MarkZuckerberg or RealZuckerberg
- Elon Musk -> ElonMusk

Your task is to come-up with character handle. Your response would be single bot handle so that our backend can copy it.

Do not use "Bot" in the handle!
"""


async def generate_handle(request: QueryRequest, create_args, generation_state: GenerationState):
    request.query = [
        ProtocolMessage(
            role="system",
            content=system
        ),
        ProtocolMessage(
            role="user",
            content="Your task is to come-up with Character handle. Your response would be single bot name so that "
                    "our backend can copy it.\n"
                    "Bot name:\n"
                    "Akinator"
        ),
        ProtocolMessage(
            role="bot",
            content="IAmAkinator"
        ),
        ProtocolMessage(
            role="user",
            content="Your task is to come-up with Character handle. Your response would be single bot name so that "
                    "our backend can copy it.\n"
                    "Bot name:\n"
                    f"{generation_state.name}"
        ),
    ]
    async for msg in stream_request(request, TEXT_MODEL, request.access_key):
        yield msg.text
