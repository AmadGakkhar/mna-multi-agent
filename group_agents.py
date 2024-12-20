import autogen
from autogen import ConversableAgent, register_function
import os
from configs import OAI_CONFIG
from prompts import (
    project_manager_prompt,
    motivational_coach_prompt,
    strategy_prompt,
    dummy_client_prompt,
    strategy_prompt_1,
    strategy_prompt_3,
    strategy_prompt_2,
)
from tools import save_to_markdown


pm = ConversableAgent(
    "pm",
    system_message=strategy_prompt_2,
    llm_config=OAI_CONFIG,
    code_execution_config=False,
    function_map=None,
    human_input_mode="NEVER",
    description="Develop a detailed Acquisition Strategy for the client.",
    # Never ask for human input.
)


dummy_client = ConversableAgent(
    "dummy_client",
    system_message=dummy_client_prompt,
    llm_config=OAI_CONFIG,
    code_execution_config=False,
    function_map=None,
    human_input_mode="ALWAYS",
)


human_proxy = ConversableAgent(
    "human_proxy",
    llm_config=False,  # no LLM used for human proxy
    human_input_mode="ALWAYS",  # always ask for human input
)