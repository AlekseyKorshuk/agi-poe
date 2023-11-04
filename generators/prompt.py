from fastapi_poe.client import stream_request
from fastapi_poe.types import QueryRequest, ProtocolMessage

from utils import GenerationState


async def generate_prompt(request: QueryRequest, create_args, generation_state: GenerationState):
    # Access the previously generated handle, bio, and greeting message.
    handle = generation_state.handle
    bio = generation_state.bio

    # Construct a character directive for the GPT-3.5 Turbo model.
    character_directive = f"You are the character {handle}. {bio} Stay in character when interacting with the user. " \
                          "Your responses should reflect the personality and characteristics outlined in your bio. " \
                          "Engage with users in a manner that is coherent with your backstory and abilities."

    # Construct a starting line for user interaction.
    start_interaction = "When users interact with you, they are looking for an immersive experience. Begin your interaction with them by staying in character."

    # Assemble the full prompt for the GPT-3.5 Turbo model.
    full_prompt = f"{character_directive}\n\n{start_interaction}"

    # Yield the full prompt as the output for the function.
    yield full_prompt

