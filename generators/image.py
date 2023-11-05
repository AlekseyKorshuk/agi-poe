from fastapi_poe.client import stream_request
from fastapi_poe.types import QueryRequest, ProtocolMessage, PartialResponse

from utils import GenerationState


async def generate_image(request: QueryRequest, create_args, generation_state: GenerationState):
    request.query = [
        ProtocolMessage(
            role="user",
            content="Your task is to write a Text2Image prompt for StableDiffusion that will generate the avatar for "
                    "the given character based on its description. The prompt should be only one sentence max (ten words!). Your "
                    "reply should contain only the prompt for Text2Image, so our backend can copy this text.\n "
                    "Description:\n"
                    f"{generation_state.bio}"
        ),
    ]
    output = ""
    async for msg in stream_request(request, "GPT-4", request.access_key):
        output += msg.text
    request.query = [
        ProtocolMessage(
            role="user",
            content=output
        ),
    ]
    async for msg in stream_request(request, "ImgXL_PixarStyleRC", request.access_key):
        if "Generating image" in msg.text:
            continue
        yield msg.text
