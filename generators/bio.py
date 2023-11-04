from fastapi_poe.client import stream_request
from fastapi_poe.types import QueryRequest, ProtocolMessage

from utils import GenerationState

async def generate_bio(request: QueryRequest, create_args, generation_state: GenerationState):
    # Convert the conversation history into a single string.
    conversation = "\n\n".join(f"{message.role}: {message.content}" for message in request.query)
    
    # Create the prompt for the model to generate a biography for the bot.
    system_message = "You are an assistant tasked with generating a biography for a chatbot. " \
                     "This biography should explain the bot's purpose, capabilities, and the type of interaction " \
                     "users can expect."

    user_message = f"Based on the provided details, create a biography for a fictional character named {generation_state.handle} (the chatbot described in the conversation above:\n\n{conversation}\n\n)" \
                "The biography should describe Fox's appearance, behavior, and environment in a manner that is " \
                "charming, narrative, and fitting for a storybook character." \
                "The biography should articulate the bot's functionality, user interaction, and any unique " \
                "features it may have. It should set clear expectations for the user experience. " \
                "Write in a professional, engaging tone and keep the description concise. " \
                "Do not output anything else, except for the bio."
                   
    # Assemble the protocol messages for the model.
    request.query = [
        ProtocolMessage(role="system", content=system_message),
        ProtocolMessage(role="user", content=user_message)
    ]

    # Stream the request to the GPT-3.5 model and yield the responses.
    async for msg in stream_request(request, "GPT-3.5-Turbo", request.access_key):
        # Ensure that the response is text and fits the context of a character biography.
        yield msg.text  # Remove any extra whitespace from the biography.
