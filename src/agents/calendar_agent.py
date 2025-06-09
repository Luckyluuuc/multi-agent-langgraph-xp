from langgraph.prebuilt import create_react_agent
from tools.tools import schedule_meeting, check_calendar_availability
from src.supervisor_agents.configuration_supervisor import Configuration
from langchain_core.runnables import RunnableConfig
class CalendarAgent:
    """
    This class creates a react agent that can schedule meetings and check calendar availability.
    """
    def __init__(self, llm, config:Configuration, handoff_tools=False):
        """
        Args:
            llm: The LLM object to use for the agent.
            config: The configuration object containing the profile and prompt.
            handoff_tools: If True, add the transfer tools to the agent (needed for swarm architecture).
        """
        self.llm = llm
        self.config = RunnableConfig(config)
        self.tools = [schedule_meeting, check_calendar_availability]

        #-----------maybe a better way to do this? for the swarm architecture------------------
        if handoff_tools:
            # If we are in a swarm architecture, we need to add the transfer tools to the agent so it can transfer a task to another agent
            from tools.tools import transfer_memory, transfer_email
            self.tools.append(transfer_memory)
            self.tools.append(transfer_email)
        #-----------------------------------------------------------
        self.agent = create_react_agent(self.llm, self.tools, prompt=self.create_prompt, name="calendar_agent")

    def create_prompt(self, state):
        return [
            {"role": "system", "content": self.config["calendar_prompt"].format(**self.config["profile"])}
        ] + state['messages']

    def get_agent(self):
        return self.agent


