from utils import GenerationState


async def generate_handle(create_args, generation_state: GenerationState):
    for msg in ["This", " is", " handle"]:
        yield msg
