import streamlit as st
from prompts import strategy_prompt_2, dummy_client_prompt
from configs import OAI_CONFIG
from autogen import ConversableAgent
import asyncio


class TrackableConversableAgent(ConversableAgent):

    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
        return super()._process_received_message(message, sender, silent)


# Initialize the agents
pm = TrackableConversableAgent(
    "pm",
    system_message=strategy_prompt_2,
    llm_config=OAI_CONFIG,
    code_execution_config=False,
    function_map=None,
    human_input_mode="NEVER",
)

human_proxy = TrackableConversableAgent(
    "human_proxy",
    llm_config=False,
    human_input_mode="ALWAYS",
)


user_input = st.text_input("Enter your message:")

if "chat_initialized" not in st.session_state:

    asyncio.run(human_proxy.a_initiate_chat(pm, message=user_input))
    st.session_state.chat_initialized = True
