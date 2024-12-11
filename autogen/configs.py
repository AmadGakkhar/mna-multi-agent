import os
from dotenv import load_dotenv

load_dotenv()


OAI_CONFIG = {
    "config_list": [
        {
            "model": os.environ["oai_model"],
            "api_key": os.environ["openai_api_key"],
        }
    ],
    "timeout": 120,
    "temperature": 0.1,
    "cache_seed": None,
}

GEMINI_CONFIG = {
    "config_list": [
        {
            "model": os.environ["gemini_model"],
            "api_key": os.environ["gemini_api_key"],
            "api_type": "google",
        }
    ],
    "timeout": 120,
    "temperature": 0.1,
    "cache_seed": None,
}
