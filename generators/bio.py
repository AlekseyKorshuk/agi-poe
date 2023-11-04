from utils import GenerationState


async def generate_bio(create_args, generation_state: GenerationState):
    for msg in ["This", " is", " bio"]:
        yield msg
