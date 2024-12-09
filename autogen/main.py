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


def save_to_markdown(
    content: str,
) -> None:
    """
    Save the given content to a markdown file.

    Parameters:
    content (str): The content to be saved.
    filename (str): The name of the markdown file. Default is 'output.md'.
    """
    filename = "output.md"
    with open(filename, "w") as file:
        file.write("# Report\n\n")
        file.write(content)
    print(f"Content written to {filename}")


pm = ConversableAgent(
    "pm",
    system_message=strategy_prompt_2,
    llm_config=OAI_CONFIG,
    code_execution_config=False,
    function_map=None,
    human_input_mode="NEVER",  # Never ask for human input.
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

register_function(
    save_to_markdown,
    caller=dummy_client,  # The agent can suggest calls to the tool.
    executor=pm,  # The  agent can execute the tool calls.
    name="save_to_markdown",  # By default, the function name is used as the tool name.
    description="Save the given content to a markdown file.",  # A description of the tool.
)


result = dummy_client.initiate_chat(
    pm,
    message="Hello",
)
