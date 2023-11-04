from fastapi_poe.client import stream_request
from fastapi_poe.types import QueryRequest, ProtocolMessage

from utils import GenerationState


async def generate_handle(request: QueryRequest, create_args, generation_state: GenerationState):
    for msg in ["This", " is", " handle"]:
        yield msg

    conversation = ""
    for message in request.query:
        conversation += f"{message.role}: {message.content}\n\n"
    request.query = [
        ProtocolMessage(
            role="system",
            content="You are an expert in ChatBots."
        ),
        ProtocolMessage(
            role="user",
            content="Your task is to come-up with ChatBot name/handle that should be unique and use 4-20 characters, "
                    "including letters, numbers, dashes and underscores. YOur resposne whould be single bot name so "
                    "that our backend can copy it. And here is our conversation with user that asks to create a bot:\n "
                    f"{conversation}"
        ),
    ]
    async for msg in stream_request(request, "GPT-3.5-Turbo", request.access_key):
        yield msg.text
