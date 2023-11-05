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


def get_full_response(generation_state):
    return f"### Bot handle\n" \
           f"```text\n" \
           f"{generation_state.handle}\n" \
           f"```\n" \
           f"### Prompt\n" \
           f"```text\n" \
           f"{generation_state.prompt}\n" \
           f"```\n" \
           f"### Greeting message\n" \
           f"```text\n" \
           f"{generation_state.greeting_message}\n" \
           f"```\n" \
           f"### Bio\n" \
           f"```text\n" \
           f"{generation_state.bio}\n" \
           f"```\n"
