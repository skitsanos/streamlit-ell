import logging
import os
from typing import List

import ell
import streamlit as st
from ell import Message
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from tools import weather

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
SUPPORTED_MODELS = {
    "gpt-4o-mini": "GPT-4 Mini",
    "gpt-4o": "GPT-4"
}
DEFAULT_MODEL = "gpt-4o-mini"

# Initialize ELL
ell.init(store='./logdir')

if "model" not in st.session_state:
    st.session_state.model = DEFAULT_MODEL
if "messages" not in st.session_state:
    st.session_state.messages = []


def validate_api_key() -> None:
    """Validate that the OpenAI API key is present in environment variables."""
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in environment variables")


def update_selected_model() -> None:
    """Update the selected model and validate it."""
    selected_model = st.session_state.model or DEFAULT_MODEL
    if selected_model not in SUPPORTED_MODELS:
        st.error(f"Unsupported model: {selected_model}")
        st.session_state.model = DEFAULT_MODEL
    st.markdown(f"> Switched to *{SUPPORTED_MODELS[selected_model]}* model")


@ell.complex(model=st.session_state.model or DEFAULT_MODEL,
             tools=[weather.get_weather],
             temperature=0.0)
def execute_with_tools(message_history: List[Message]) -> Message:
    """
    Execute the chat completion with tools.

    Args:
        message_history: List of previous messages

    Returns:
        Message: The response message from the model
    """
    return message_history


def chat_with_gpt() -> str:
    """
    Process chat messages and handle tool execution.

    Returns:
        str: The response text to display to the user
    """
    try:
        llm_response = execute_with_tools(st.session_state.messages)

        if llm_response.tool_calls:
            logger.info("Tool execution requested")
            try:
                tool_results = llm_response.call_tools_and_collect_as_message()
                final_response = execute_with_tools(
                    st.session_state.messages + [llm_response, tool_results]
                )
                return final_response.text
            except Exception as e:
                logger.error(f"Tool execution failed: {str(e)}")
                return f"I encountered an error while processing tools: {str(e)}"
        else:
            return llm_response.text
    except Exception as e:
        logger.error(f"Chat execution failed: {str(e)}")
        return "I'm sorry, but I encountered an error processing your request."


def main():
    """Main application function."""
    try:
        # Validate API key
        validate_api_key()

        # Set page configuration
        st.set_page_config(page_title="Chat with GPT", page_icon="💭")

        # Sidebar
        with st.sidebar:
            st.title("Chat with GPT")

            st.selectbox(
                "Model",
                list(SUPPORTED_MODELS.keys()),
                index=list(SUPPORTED_MODELS.keys()).index(DEFAULT_MODEL),
                key="model",
                on_change=update_selected_model
            )

        # Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message.role):
                st.markdown(message.text)

        # Accept user input
        if prompt := st.chat_input("What's on your mind?"):
            # Add user's message to chat history
            st.session_state.messages.append(
                ell.user(content=prompt)
            )

            # Display the user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = chat_with_gpt()
                    st.markdown(response)

            # Add assistant response to chat history
            st.session_state.messages.append(ell.assistant(response))

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
