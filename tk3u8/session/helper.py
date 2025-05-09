import random
from tk3u8.constants import USER_AGENT_LIST


def get_random_user_agent() -> str:
    return random.choice(USER_AGENT_LIST)
