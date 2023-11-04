from dataclasses import dataclass


@dataclass
class GenerationState:
    handle: str = ""
    bio: str = ""
    prompt: str = ""
    greeting_message: str = ""


def parse_args(content):
    command_parts = content.strip().split(" ", 1)[1]
    seed_args = dict(part.split(":") for part in command_parts.split(";"))
    seed_args['categories'] = seed_args['categories'].split(",")
    seed_args['personalities'] = seed_args['personalities'].split(",")
    return seed_args
