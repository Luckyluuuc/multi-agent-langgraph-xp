
from model.model import Model
from langgraph_swarm import create_swarm
from agents.email_agent import EmailAgent
from agents.memory_agent import MemoryAgent
from agents.calendar_agent import CalendarAgent
from src.swarm_agents.configuration_swarm import Configuration
from langchain_core.runnables import RunnableConfig
from swarm_agents.state import InputState, OutputState, OverallState
from langgraph.graph import StateGraph, START
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage


class Swarm: 
    """
    Class to manage the swarm of agents. 
    This class is responsible for initializing the agents and creating the swarm architecture.

    We encapsulated the swarm graph in an other graph to be able to choose the starting point of the graph.
    The starting point can be either a message from the user or a new email.
    """
    def __init__(self):
        self.config = RunnableConfig(Configuration())
        self.llm = Model(name=self.config["model"], local=True).initialize_and_get_model()

        # Initialize agents
        self.memory_agent = MemoryAgent(llm=self.llm, config=self.config, handoff_tools=True)
        self.email_agent = EmailAgent(llm=self.llm, config=self.config, handoff_tools=True)
        self.calendar_agent = CalendarAgent(self.llm, config=self.config, handoff_tools=True)

        self.swarm = create_swarm(
            agents=[self.email_agent.get_agent(), self.calendar_agent.get_agent(), self.memory_agent.get_agent()],
            default_active_agent="memory_agent",
        ).compile()

        self.graph = self.build_graph()

    def build_graph(self):

        builder = StateGraph(OverallState, input=InputState, output=OutputState, config_schema=self.config)

        builder.add_node(
            "input_router", 
            self.starting_root)
        
        builder.add_node(
            "swarm", 
            self.swarm)
        
        builder.add_edge(START, "input_router")
        builder.add_edge("input_router", "swarm")

        return builder.compile()

    def get_compiled_swarm(self):
        return self.swarm
    
    def get_compiled_graph(self):
        return self.graph
    
    def starting_root(self, state:OverallState): 
        """This is a node (with Command) that will start the graph wether the starting point is a message of the user or a new email"""

        entry = state.get("entry", "user") #default to user if not specified

        if entry == "user":
            message = state["input"]
            update={"messages": [HumanMessage(content=message)], "active_agent": state.get("active agent", "memory_agent")}
        elif entry == "email":
            message = self.config["email_input_prompt"].format(email_input=state["input"])
            update={"messages": [HumanMessage(content=message)], "active_agent": state.get("active agent", "email_agent")}
        else :
            raise ValueError("Invalid entry point. Must be 'user' or 'email'.")
        
        return update

    


if __name__ == "__main__":
    # Initialize the swarm
    swarm_instance = Swarm()
    compiled_graph = swarm_instance.get_compiled_graph()

    input = {
        "input": "Please send an email to John Doe with the subject 'Meeting Reminder' and the content 'Don't forget about our meeting tomorrow at 10 AM.'",
        "entry": "user",
    }


    # Let's print the messages in a nice way : 

    for step in compiled_graph.stream(
        input,
        stream_mode="updates",
    ):
        print("step : ", step)
        for _, update in step.items():
                if update is not None:
                    print(update)
                    for message in update.get("messages", []):
                            message.pretty_print()



        