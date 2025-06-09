from typing_extensions import TypedDict, Optional, Literal
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

from typing import Annotated



#this 
class InputState(TypedDict):
    """State of the agent."""
    input : str #could be a message from the user or a new email
    entry: Literal["user", "email"]


class OutputState(TypedDict):
    messages: Optional[Annotated[list, add_messages]]
    active_agent: Optional[str] #the agent that is currently active

class OverallState(InputState, OutputState):
    """Overall state of the agent."""
    pass


