import os
from dotenv import load_dotenv

load_dotenv()


OAI_CONFIG = {
    "config_list": [
        {
            "model": os.environ["model"],
            "api_key": os.environ["openai_api_key"],
        }
    ],
    "timeout": 120,
    "temperature": 0.1,
}
