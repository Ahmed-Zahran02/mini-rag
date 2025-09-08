from helpers import Settings, get_settings
import os
import random
import string


class BaseController:
    def __init__(self, app_settings: Settings = get_settings()):
        self.app_settings = app_settings

    def generate_random_string(self, length: int = 12) -> str:
        """Generate a random string with the given length."""
        characters = string.ascii_letters + string.digits
        random_string = "".join(random.choice(characters) for _ in range(length))
        return random_string
