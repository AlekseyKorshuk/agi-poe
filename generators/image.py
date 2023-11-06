from fastapi_poe.client import stream_request
from fastapi_poe.types import QueryRequest, ProtocolMessage, PartialResponse

from config import TEXT_MODEL, IMAGE_MODEL
from utils import GenerationState


async def generate_image(request: QueryRequest, create_args, generation_state: GenerationState):
    request.query = [
        ProtocolMessage(
            role="user",
            content=f"""Generate an avatar based on the description provided, suitable for small screens and profile images, without resembling a 'Bot'/'Robot'/'ChatBot'. Use gender if specified. The final avatar will be post-processed for a Pixar-like appearance. Your response should only include the Text2Image prompt. Keep it concise, no more than seven words. Avoid policy violations. 

Examples:
1. Red-hatted plumber, brown boots
2. Cute fluffy llama, large reflective eyes
3. Yoda
4. Knight in blue, glowing sword, dragon shield
5. Whimsical fairy, iridescent wings, glowing hair
6. Cybernetic wolf, neon detail, holographic eyes

Prompt:
{generation_state.prompt}
"""
        ),
    ]
    output = ""
    async for msg in stream_request(request, TEXT_MODEL, request.access_key):
        output += msg.text
    print(output)
    request.query = [
        ProtocolMessage(
            role="user",
            content=output
        ),
    ]
    async for msg in stream_request(request, IMAGE_MODEL, request.access_key):
        if "Generating image" in msg.text:
            continue
        yield msg.text
