from fastapi_poe.client import stream_request
from fastapi_poe.types import QueryRequest, ProtocolMessage

from config import TEXT_MODEL
from utils import GenerationState

system = """You are an expert in Characters. You are able to create Characters by parts: name, bio, greeting message, prompt.
You are specialized in name for bots. The Bot name should be engaging to click on the website.

Examples of good names:
- ML Engineer
- Jake Classmate
- Read My Mind
- Music Generator
- Akinator
- Vampire Queen
- Mark Zuckerberg (CEO of Meta)
- Elon Musk

Your task is to come-up with character name. Your response would be single bot name so that our backend can copy it.
I will provide you with AI conversation with User that asks to create a bot.

Do not use "Bot" in the name!
"""


async def generate_name(request: QueryRequest, create_args, generation_state: GenerationState):
    conversation = "\n\n".join(f"{message.role}: {message.content}" for message in request.query[1:])

    request.query = [
        ProtocolMessage(
            role="system",
            content=system
        ),
        ProtocolMessage(
            role="user",
            content="Your task is to come-up with Character name. Your response would be single bot name so that "
                    "our backend can copy it.\n"
                    "I will provide you with AI conversation with User that asks to create a bot:\n"
                    f"user: I want a bot that guesses my number"
        ),
        ProtocolMessage(
            role="bot",
            content="Number Guesser"
        ),
        ProtocolMessage(
            role="user",
            content="Your task is to come-up with Character name. Your response would be single bot name so that "
                    "our backend can copy it.\n"
                    "I will provide you with AI conversation with User that asks to create a bot:\n"
                    f"user: Mark Zuckerberg (CEO of Meta)"
        ),
        ProtocolMessage(
            role="bot",
            content="Mark Zuckerberg (CEO of Meta)"
        ),
        ProtocolMessage(
            role="user",
            content="Your task is to come-up with Character name. Your response would be single bot name so that "
                    "our backend can copy it.\n"
                    "I will provide you with AI conversation with User that asks to create a bot:\n"
                    f"user: I want to talk with a cow living in a forest"
        ),
        ProtocolMessage(
            role="bot",
            content="Birch Cow"
        ),
        ProtocolMessage(
            role="user",
            content="Your task is to come-up with Character name. Your response would be single bot name so that "
                    "our backend can copy it.\n"
                    "I will provide you with AI conversation with User that asks to create a bot:\n"
                    f"{conversation}"
        ),
    ]
    async for msg in stream_request(request, TEXT_MODEL, request.access_key):
        yield msg.text
