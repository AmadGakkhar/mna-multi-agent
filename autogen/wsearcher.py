import os
import autogen
from autogen import ConversableAgent, register_function, GroupChatManager, GroupChat
from autogen.agentchat.contrib.web_surfer import WebSurferAgent
from configs import OAI_CONFIG, SUMMARISER_CONFIG, GEMINI_CONFIG
from prompts import *
from utils import read_markdown_file


strategy_report = read_markdown_file(
    "/home/amadgakkhar/Microsoft_Acquisition_Strategy_Agriculture.md"
)


user_proxy = ConversableAgent(
    "user_proxy", llm_config=OAI_CONFIG, human_input_mode="ALWAYS"
)

web_surfer = WebSurferAgent(
    "web_surfer",
    llm_config=OAI_CONFIG,
    summarizer_llm_config=SUMMARISER_CONFIG,
    browser_config={"viewport_size": 4096, "bing_api_key": os.environ["bing_api_key"]},
    is_termination_msg=lambda msg: "`TERMINATE`" in msg["content"],
)

researcher = ConversableAgent(
    "researcher",
    system_message=researcher_prompt_3,
    llm_config=OAI_CONFIG,
    code_execution_config=False,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "`TERMINATE`" in msg["content"],
)

web_surfer.initiate_chat(
    researcher,
    message=f"Here is the acquisition strategy report. Generate search queries based on the target profile, then execute them sequentially:\n\n{strategy_report}",
)
