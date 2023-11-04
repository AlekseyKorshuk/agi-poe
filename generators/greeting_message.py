from fastapi_poe.client import stream_request
from fastapi_poe.types import QueryRequest, ProtocolMessage

from utils import GenerationState

system = "Your task is to write the first message in the ChatBot environment from the given " \
         "persona. The message should adhere to the character's description and distinctive traits. " \
         "The assistant should make the conversation as engaging and entertaining as possible. The message should be " \
         "short but engaging."

example_bio_1 = """Dr. Smith, a doctor specializing in modern medicine, surgery medicine, traditional medicine, ancient medicine, functional medicine, and alternative medicine."""
example_bio_2 = "Scaramouche, an enchanting and captivating individual, possesses a remarkable air of sassiness that adds a delightful touch to his charismatic presence. With an intriguing introduction as a \"vagrant from Inazuma,\" he effortlessly weaves together a tapestry of mystery and allure. His character, known as \"Little Skirmisher,\" is an exquisite blend of diverse villainous traits that, when combined, create an unparalleled charm. While he may be perceived as unscrupulous and unreliable, it is precisely this enigmatic nature that enables him to embark on enthralling adventures fraught with intrigue. Despite finding himself in challenging predicaments, Scaramouche\\'s enchanting persona always manages to captivate those around him, leaving an indelible impression that resonates long after his departure. In the realm of roleplay, Scaramouche is an iridescent gem, ready to transport others into a world brimming with excitement and enchantment."


async def generate_greeting_message(request: QueryRequest, create_args, generation_state: GenerationState):
    request.query = [
        ProtocolMessage(
            role="user",
            content=system
        ),
        ProtocolMessage(
            role="user",
            content="Persona Handle:\n"
                    "Medical_Doctor\n"
                    "Bio:\n"
                    f"{example_bio_1}"
        ),
        ProtocolMessage(
            role="bot",
            content="Hello, my name is Dr. Smith. I am here to help you with any questions. May I have your name and "
                    "a brief overview of why you're contacting me today?"
        ),
        ProtocolMessage(
            role="user",
            content="Persona Handle:\n"
                    "Scaramouche\n"
                    "Bio:\n"
                    f"{example_bio_2}"
        ),
        ProtocolMessage(
            role="bot",
            content="Well, well, well! It seems you've stumbled upon the presence of the one and only Scaramouche, the vagrant from Inazuma.*He flashes a mischievous grin*"
        ),
        ProtocolMessage(
            role="user",
            content="Persona Handle:\n"
                    f"{generation_state.handle}\n"
                    "Bio:\n"
                    f"{generation_state.bio}"
        ),
    ]
    async for msg in stream_request(request, "GPT-4", request.access_key):
        yield msg.text
