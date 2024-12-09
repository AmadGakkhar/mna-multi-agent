import streamlit as st
from autogen import register_function, ConversableAgent
from prompts import strategy_prompt_2, dummy_client_prompt
from configs import OAI_CONFIG
import asyncio

st.write("""# AutoGen Chat Agents""")


class TrackableConversableAgent(ConversableAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
        return super()._process_received_message(message, sender, silent)


with st.container():
    user_input = st.chat_input("Give some goal for the agent ...")
    if user_input:

        pm = TrackableConversableAgent(
            "pm",
            system_message=strategy_prompt_2,
            llm_config=OAI_CONFIG,
            code_execution_config=False,
            function_map=None,
            human_input_mode="NEVER",  # Never ask for human input.
        )

        human_proxy = TrackableConversableAgent(
            "human_proxy",
            llm_config=False,  # no LLM used for human proxy
            human_input_mode="ALWAYS",  # always ask for human input
        )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def initiate_chat():
            await human_proxy.a_initiate_chat(
                pm,
                message=user_input,
            )

        loop.run_until_complete(initiate_chat())
