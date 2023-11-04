from fastapi_poe.client import stream_request
from fastapi_poe.types import QueryRequest, ProtocolMessage

from utils import GenerationState

async def generate_handle(request: QueryRequest, create_args, generation_state: GenerationState):
    # Accumulate the conversation history in a formatted string.
    conversation = "\n\n".join(f"{message.role}: {message.content}" for message in request.query)
    
    # Define the bot's task clearly and concisely.
    system_message = "You are a creative expert tasked with generating unique and catchy names for ChatBots. " \
                     "Each name should adhere to the following criteria: " \
                     "be 4-20 characters in length, " \
                     "only contain letters, numbers, dashes, and underscores, " \
                     "and be a single name suggestion per response for backend processing."

    user_message = f"Here is our conversation with a user requesting a bot name:\n\n{conversation}\n\n" \
                   "Given this conversation, suggest a suitable name for the ChatBot."
    
    # Construct the protocol messages to send to the model.
    request.query = [
        ProtocolMessage(role="system", content=system_message),
        ProtocolMessage(role="user", content=user_message)
    ]

    # Stream the request to the GPT-3.5 model and yield the responses.
    async for msg in stream_request(request, "GPT-3.5-Turbo", request.access_key):
        # Ensure the response is text-only as we expect a single bot name.
        yield msg.text.strip()  # Strip any extra whitespace from the name.

