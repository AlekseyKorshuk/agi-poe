from utils import GenerationState


async def generate_greeting_message(create_args, generation_state: GenerationState):
    for msg in ["This", " is", " greeting_message"]:
        yield msg
