
import uuid
from tools.tools import check_calendar_availability, schedule_meeting, write_email, search_address, manage_memory_tool, search_memory_tool
from model.embedding import Embddings
from model.model import Model
from langgraph.store.memory import InMemoryStore
from langgraph_bigtool import create_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


# Define the tools to be used in the agent
all_tools = [
    check_calendar_availability,
    schedule_meeting,
    write_email,
    search_address,
    manage_memory_tool,
    search_memory_tool,
]

# Register tools with unique IDs
tool_registry = {
    str(uuid.uuid4()): tool
    for tool in all_tools
}

# Index tool names and descriptions in the LangGraph
# Store. Here we use a simple in-memory store.
embeddings = Embddings().get_embedding_obj()

store = InMemoryStore(
    index={
        "embed": embeddings,
        "fields": ["description"],
    }
)
for tool_id, tool in tool_registry.items():
    store.put(
        ("tools",),
        tool_id,
        {
            "description": f"{tool.name}: {tool.description}",
        },
    )

# Initialize the LLM model
llm = Model(name="qwen2.5:14b-instruct", local=True).initialize_and_get_model()

builder = create_agent(llm, tool_registry)
bigtool_agent = builder.compile() #This create the object for the langgraph studio (for visualization only)
bigtool_agent_with_store = builder.compile(store=store) #This create the "real" object that we can use in the shell


if __name__ == "__main__":
    # Example usage of the bigtool_agent

    query = "Use available tools to schedule a meeting with John Doe on 2023-10-01 at 9:00 AM."

    # Test it out
    for step in bigtool_agent_with_store.stream(
        {"messages": query},
        stream_mode="updates",
    ):
        for _, update in step.items():
            for message in update.get("messages", []):
                message.pretty_print()