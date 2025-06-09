from langgraph.prebuilt import create_react_agent
from tools.tools import manage_memory_tool, search_memory_tool, transfer_calendar, transfer_email
from src.supervisor_agents.configuration_supervisor import Configuration
from langchain_core.runnables import RunnableConfig

class MemoryAgent:
    """
    React agent for managing memory in the agent system.
    
    """

    def __init__(self, llm, config:Configuration, handoff_tools=False):
        """
        Args:
            llm: The LLM object to use for the agent.
            config: The configuration object containing the profile and prompt.
            handoff_tools: If True, add the transfer tools to the agent (needed for swarm architecture).
        """ 
        self.config = RunnableConfig(config)
        self.llm = llm
        self.tools = [manage_memory_tool, search_memory_tool]

        #-----------maybe a better way to do this? for the swarm architecture------------------
        if handoff_tools: 
            from tools.tools import transfer_calendar, transfer_email
            self.tools.append(transfer_calendar)
            self.tools.append(transfer_email)
        #-----------------------------------------------------------


        self.agent = create_react_agent(self.llm, self.tools, prompt=self.create_prompt, name="memory_agent")

    def create_prompt(self, state):
        return [
            {
                "role": "system",
                "content": self.config["memory_prompt"].format(**self.config["profile"])
            }
        ] + state['messages']


    def get_agent(self):
        return self.agent

    

if __name__ == "__main__":
    pass


    
    