from tools.tools import write_email, search_address
from langgraph.prebuilt import create_react_agent
from src.supervisor_agents.configuration_supervisor import Configuration
from langchain_core.runnables import RunnableConfig
from model.model import Model

class EmailAgent:
    """
    This class creates a react agent that can send emails and search for addresses.
    """
    def __init__(self, llm, config, handoff_tools=False): 
        """
        Args:
            llm: The LLM object to use for the agent.
            config: The configuration object containing the profile and prompt.
            handoff_tools: If True, add the transfer tools to the agent (needed for swarm architecture).
        """
        self.llm = llm
        self.config = RunnableConfig(config)
        self.tools = [write_email, search_address]

        #-----------maybe a better way to do this? for the swarm architecture------------------
        if handoff_tools:     
            from tools.tools import transfer_calendar, transfer_memory
            self.tools.append(transfer_calendar)
            self.tools.append(transfer_memory)
        #-----------------------------------------------------------
        self.agent = create_react_agent(self.llm, self.tools, config_schema=self.config, prompt=self.create_prompt, name="email_agent")
        
        

    def create_prompt(self, state):
        return [
            {
                "role": "system",
                "content": self.config['email_prompt'].format(**self.config['profile'])

            }
        ] + state['messages']


    def get_agent(self):
        return self.agent
    

if __name__ == "__main__":
    config = RunnableConfig(Configuration())
    llm = Model(name=config["model"], local=True).initialize_and_get_model()
    emailagent = EmailAgent(llm=llm, config=config).get_agent()
    response = emailagent.invoke(
    {"messages": [{
        "role": "user", 
        "content": "Please send an email to John Doe with the subject 'Meeting Reminder' and the content 'Don't forget about our meeting tomorrow at 10 AM.'"
    }]})

    print("Final response:")
    print(response)

    print("----------------")
    for m in response['messages']:
        m.pretty_print()


    