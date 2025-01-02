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
    critic_prompt,
)
from tools import (
    save_to_markdown,
    read_from_markdown,
    get_options,
    get_companies,
    get_number_of_companies,
    get_names_and_summaries,
    save_response_json,
)

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

critic = ConversableAgent(
    "critic",
    llm_config=LLM_CONFIG,
    system_message=critic_prompt,
    human_input_mode="NEVER",
)


executor = ConversableAgent(
    "executor",
    llm_config=False,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: msg.get("content") is not None
    and "TERMINATE" in msg["content"],
    default_auto_reply="",
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
    caller=researcher,  # Add multiple callers here
    executor=executor,
    name="get_companies",
    description="Retrieve companies based on specified filters.",
)
register_function(
    get_names_and_summaries,
    caller=researcher,  # Add multiple callers here
    executor=executor,
    name="get_names_and_summaries",
    description="Get the names and summaries of companies from the JSON file.",
)

## Critic Functions

register_function(
    read_from_markdown,
    caller=critic,
    executor=executor,
    name="read_from_markdown",
    description="Read the content from a markdown file.",
)
register_function(
    get_names_and_summaries,
    caller=critic,  # Add multiple callers here
    executor=executor,
    name="get_names_and_summaries",
    description="Get the names and summaries of companies from the JSON file.",
)

register_function(
    save_response_json,
    caller=critic,  # Add multiple callers here
    executor=executor,
    name="save_response_json",
    description="Save the given JSON string to a file.",
)


researcher.register_nested_chats(
    trigger=human_proxy,
    chat_queue=[
        {
            "sender": executor,
            "recipient": researcher,
            "message": "Which tool you want to call?",
            # "max_turns": 5,
        },
        {
            "sender": executor,
            "recipient": critic,
            "message": "Which tool you want to call?",
        },
    ],
)

human_proxy.initiate_chat(
    researcher,
    message="Hello",
)
