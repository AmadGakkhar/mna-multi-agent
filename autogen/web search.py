import autogen
from autogen import ConversableAgent, register_function
from autogen.agentchat.contrib.web_surfer import WebSurferAgent  # noqa: E402import os
from configs import OAI_CONFIG, SUMMARISER_CONFIG, GEMINI_CONFIG
from prompts import *
import os

searcher = ConversableAgent(
    "Searcher",
    llm_config=OAI_CONFIG,
    code_execution_config=False,
    human_input_mode="NEVER",  # Never ask for human input.
)

web_surfer = WebSurferAgent(
    "web_surfer",
    llm_config=OAI_CONFIG,
    summarizer_llm_config=SUMMARISER_CONFIG,
    browser_config={"viewport_size": 4096, "bing_api_key": os.environ["bing_api_key"]},
)

user_proxy = ConversableAgent(
    "user_proxy", llm_config=OAI_CONFIG, human_input_mode="ALWAYS"
)


result = user_proxy.initiate_chat(web_surfer, message="Search articles about AI")
