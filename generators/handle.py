from fastapi_poe.client import stream_request
from fastapi_poe.types import QueryRequest, ProtocolMessage

from utils import GenerationState

system = """You are an expert in ChatBots. You are able to create ChatBots by parts: name/handle, bio, greeting message, prompt.
You are specialized in handle/name for bots. The Bot name should be engaging to click on the website.

Handle rules:
ChatBot name/handle that should be unique and use 4-20 characters, including letters, numbers, dashes and underscores.

Examples of good names:
- ML-Engineer
- Jake-Classmate
- ReadMind
- MusicGenerator
- Akinator
- VampireQueen

Your task is to come-up with ChatBot name/handle. Your response would be single bot name so that our backend can copy it.
I will provide you with AI conversation with User that asks to create a bot.
"""


async def generate_handle(request: QueryRequest, create_args, generation_state: GenerationState):
    conversation = "\n\n".join(f"{message.role}: {message.content}" for message in request.query)

    request.query = [
        ProtocolMessage(
            role="system",
            content=system
        ),
        ProtocolMessage(
            role="user",
            content="Your task is to come-up with ChatBot name/handle. Your response would be single bot name so that "
                    "our backend can copy it.\n"
                    "I will provide you with AI conversation with User that asks to create a bot:\n"
                    f"user: I want a bot that guesses my number"
        ),
        ProtocolMessage(
            role="bot",
            content="NumberGuesser"
        ),
        ProtocolMessage(
            role="user",
            content="Your task is to come-up with ChatBot name/handle. Your response would be single bot name so that "
                    "our backend can copy it.\n"
                    "I will provide you with AI conversation with User that asks to create a bot:\n"
                    f"{conversation}"
        ),
    ]
    async for msg in stream_request(request, "GPT-4", request.access_key):
        yield msg.text
