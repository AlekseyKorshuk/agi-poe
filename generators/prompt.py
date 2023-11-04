from fastapi_poe.client import stream_request
from fastapi_poe.types import QueryRequest, ProtocolMessage

from utils import GenerationState


async def generate_prompt(request: QueryRequest, create_args, generation_state: GenerationState):
    # Access the stored handle, bio, and greeting message from the generation state.
    handle = generation_state.handle
    bio = generation_state.bio
    greeting_message = generation_state.greeting_message

    # Construct the prompt that provides GPT-3.5 Turbo with the context needed to emulate the bot's character.
    prompt = (
        f"Here are the details of the chatbot named {handle}:\n\n"
        f"Bio:\n{bio}\n\n"
        f"Greeting Message:\n{greeting_message}\n\n"
        f"Using this information, you are now in character as {handle}. "
        f"Your responses should reflect {handle}'s personality and backstory as described in the bio. "
        f"Engage with users in a manner that is consistent with the greeting message, "
        f"and provide helpful, knowledgeable, and character-consistent interactions. "
        f"Maintain a storybook-like charm and whimsicality in all your conversations."
    )

    # Add the final prompt to the QueryRequest object.
    request.query.append(ProtocolMessage(role="system", content=prompt))

    # Yield the prompt text.
    yield prompt
