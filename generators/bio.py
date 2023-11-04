from fastapi_poe.client import stream_request
from fastapi_poe.types import QueryRequest, ProtocolMessage

from utils import GenerationState

async def generate_bio(request: QueryRequest, create_args, generation_state: GenerationState):
    # Convert the conversation history into a single string.
    conversation = "\n\n".join(f"{message.role}: {message.content}" for message in request.query)
    
    # Create the prompt for the model to generate a biography.
    system_message = "You are an assistant tasked with generating brief and engaging biographies. " \
                     "The biography should encapsulate relevant personal and professional details, " \
                     "highlight achievements, and be styled in a third-person narrative. It should be " \
                     "suitable for a professional profile."

    user_message = f"Based on the following conversation, create a biography for the individual described:\n\n{conversation}\n\n" \
                   "Craft the biography in a manner that is professional and engaging."
    
    # Assemble the protocol messages for the model.
    request.query = [
        ProtocolMessage(role="system", content=system_message),
        ProtocolMessage(role="user", content=user_message)
    ]

    # Stream the request to the GPT-3.5 model and yield the responses.
    async for msg in stream_request(request, "GPT-3.5-Turbo", request.access_key):
        # Ensure that the response is text and fits the context of a biography.
        yield msg.text.strip()  # Remove any extra whitespace from the biography.
