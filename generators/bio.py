from fastapi_poe.types import QueryRequest

from utils import GenerationState


async def generate_bio(request: QueryRequest, create_args, generation_state: GenerationState):
    for msg in ["This", " is", " bio"]:
        yield msg
