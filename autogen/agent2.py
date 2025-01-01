import autogen
from autogen import ConversableAgent, register_function
import os
from configs import OAI_CONFIG, GEMINI_CONFIG
from prompts import (
    project_manager_prompt,
    motivational_coach_prompt,
    strategy_prompt,
    dummy_client_prompt,
    strategy_prompt_1,
    strategy_prompt_3,
    strategy_prompt_2,
    researcher_prompt_fd,
)
from tools import save_to_markdown, read_from_markdown, get_options, get_companies

LLM_CONFIG = OAI_CONFIG
path = "/home/amadgakkhar/code/mna-multi-agent/autogen/output.md"

human_proxy = ConversableAgent(
    "human_proxy",
    llm_config=LLM_CONFIG,
    human_input_mode="ALWAYS",  # always ask for human input
)

researcher = ConversableAgent(
    "researcher",
    llm_config=LLM_CONFIG,
    system_message=researcher_prompt_fd,
    human_input_mode="NEVER",
)

print(researcher.system_message)

executor = ConversableAgent(
    "executor",
    llm_config=False,
    human_input_mode="NEVER",
    default_auto_reply="Which tool you want me to use",
)

register_function(
    read_from_markdown,
    caller=researcher,
    executor=executor,
    name="read_from_markdown",
    description="Read the content from a markdown file.",
)
register_function(
    get_options,
    caller=researcher,
    executor=executor,
    name="get_options",
    description="Retrieve options for a given parameter.",
)
register_function(
    get_companies,
    caller=researcher,
    executor=executor,
    name="get_companies",
    description="Retrieve companies based on specified filters.",
)
researcher.register_nested_chats(
    trigger=human_proxy,
    chat_queue=[
        {
            "sender": executor,
            "recipient": researcher,
            "message": "Which tool you want to call?",
            "max_turns": 4,
        }
    ],
)

human_proxy.initiate_chat(
    researcher,
    message="Hello",
)
