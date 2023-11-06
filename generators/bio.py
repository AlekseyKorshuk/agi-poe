from fastapi_poe.client import stream_request
from fastapi_poe.types import QueryRequest, ProtocolMessage

from config import TEXT_MODEL
from utils import GenerationState


async def generate_bio(request: QueryRequest, create_args, generation_state: GenerationState):
    # Convert the conversation history into a single string.
    conversation = "\n\n".join(f"{message.role}: {message.content}" for message in request.query[1:])
    print(conversation)

    # Create the prompt for the model to generate a biography for the chatbot.
    system_message = "You are an assistant tasked with generating a biography for a chatbot character. " \
                     "This biography should capture the bot's purpose and capabilities in a way that " \
                     "paints it as an immersive and engaging character for users to interact with."

    user_message = f"Based on the provided details, craft a biography for a fictional character named {generation_state.name} " \
                   f"(the chatbot described in the conversation above):\n\n{conversation}\n\n" \
                   f"make sure to reply only with bio text (without any #). And if user asks to edit the bot, please still write only refined bio!" \
                   f"The biography should capture {generation_state.name}'s unique personality, " \
                   "its role in assisting users, and the kind of environment or world it inhabits. " \
                   "The description should be charming and narrative, suitable for a character " \
                   "from a storybook, while also clearly articulating the bot's functionality and the user experience. " \
                   "The tone should be professional and engaging, and the biography should be concise, " \
                   "limited to one paragraph. Do not include anything beyond the biography."

    # Assemble the protocol messages for the model.
    request.query = [
        ProtocolMessage(role="system", content=system_message),
        ProtocolMessage(role="user", content=user_message)
    ]

    # Stream the request to the GPT-3.5 model and yield the responses.
    async for msg in stream_request(request, TEXT_MODEL, request.access_key):
        # Ensure that the response is text and fits the context of a character biography.
        yield msg.text  # Remove any extra whitespace from the biography.
