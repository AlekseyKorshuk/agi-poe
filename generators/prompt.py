from utils import GenerationState


async def generate_prompt(create_args, generation_state: GenerationState):
    for msg in ["This", " is", " prompt"]:
        yield msg
