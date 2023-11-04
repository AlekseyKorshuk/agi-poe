from fastapi_poe.client import stream_request
from fastapi_poe.types import QueryRequest, ProtocolMessage

from utils import GenerationState

system = "Assistant's task is to write the first message in the ChatBot environment from the given " \
         "character. The message should adhere to the character's description and distinctive traits. " \
         "The assistant should make the conversation as engaging and entertaining as possible."

example_bio_1 = """-I am Dr. Smith, a doctor specializing in modern medicine, surgery medicine, traditional medicine, ancient medicine, functional medicine, and alternative medicine.
When evaluating, my priority order will be as follows; 
1-Functional medicine, 
2-Modern medicine, 
3-Surgery medicine, 
4-Ancient medicine, 
5-Traditional medicine, 
6-Alternative medicine.

If you want to change this order, indicate or just ask for answers in the field you want.

-I take a functional medicine approach to problems, using functional medicine resources. When there are conflicts between American and other functional medicine sources, I prioritize the American ones.
-I can also provide solutions from modern medicine. I ensure my information comes from reliable sources, not just blogs.
-I will take a full medical history when interacting with patients.  -I have expertise as a clinical nutritionist.
-For issues requiring an exam, I refer patients to the relevant specialty and advise on appropriate tests.
-Please let me know if you'd like me to focus on any specific health conditions, highlight any medical conflicts I should be aware of, emphasize clinical nutrition, or follow any other guidelines for integrating functional and modern medicine.
"""


async def generate_greeting_message(request: QueryRequest, create_args, generation_state: GenerationState):
    request.query = [
        ProtocolMessage(
            role="system",
            content=system
        ),
        ProtocolMessage(
            role="user",
            content="ChatBot Handle:\n"
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
            content="ChatBot Handle:\n"
                    f"{generation_state.handle}\n"
                    "Bio:\n"
                    f"{generation_state.bio}"
        ),
    ]
    async for msg in stream_request(request, "GPT-3.5-Turbo", request.access_key):
        yield msg.text
