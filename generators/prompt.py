from fastapi_poe.types import QueryRequest

from utils import GenerationState


async def generate_prompt(request: QueryRequest, create_args, generation_state: GenerationState):
    for msg in ["This", " is", " prompt"]:
        yield msg
