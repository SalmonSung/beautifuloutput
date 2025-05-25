from langchain_core.messages import AIMessage, ToolMessage, HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages.base import BaseMessage
from pydantic import BaseModel
from typing import Literal, List, Union
from beautifuloutput.utils import *

def force_structure_output(
    llm: BaseChatModel,
    messages: List[Union[str, HumanMessage, SystemMessage]],
    response_format: type[BaseModel],
    format_type: Literal["pydantic"] = "pydantic"
) -> BaseMessage:
    """
    Augments the last message in a message sequence with a prompt instructing the LLM
    to output its answer in a specified (e.g., Pydantic) format, then invokes the LLM.

    Args:
        llm (BaseChatModel): The language model to invoke (must have an `invoke()` method).
        messages (List[Union[str, HumanMessage, SystemMessage]]): The conversation history.
            The last message (string or HumanMessage/SystemMessage) will have formatting instructions appended.
        response_format type[BaseModel]: A Pydantic model describing the desired output structure.
        format_type (Literal["pydantic"], optional): The type of format instructions to append. Default is "pydantic".

    Returns:
        BaseMessage: The response from the language model, structured per the appended format instructions.
    """
    format_dict = retrieve_pydantic(response_format)
    format_string = pydantic2prompt(format_dict)

    # Append format instructions to the last message
    last_message = messages[-1]
    if isinstance(last_message, str):
        messages[-1] = last_message + format_string
    elif isinstance(last_message, HumanMessage):
        messages[-1] = HumanMessage(content=last_message.content + format_string)
    elif isinstance(last_message, SystemMessage):
        messages[-1] = SystemMessage(content=last_message.content + format_string)
    else:
        raise ValueError(f"Unsupported message type: {type(last_message)}")


    return llm.invoke(messages)



