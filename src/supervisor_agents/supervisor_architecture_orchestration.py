from model.model import Model
from langgraph_supervisor import create_supervisor
from src.agents.email_agent import EmailAgent
from src.agents.calendar_agent import CalendarAgent
from src.supervisor_agents.configuration_supervisor import Configuration
from langchain_core.runnables import RunnableConfig




class Supervisor:
    """
    Class to manage a hierachical team of agents.
    """
    def __init__(self):
        self.config = RunnableConfig(Configuration())
        self.llm = Model(name=self.config["model"], local=True).initialize_and_get_model()


        # Initialize agents
        self.email_agent = EmailAgent(llm=self.llm, config=self.config)
        self.calendar_agent = CalendarAgent(self.llm, config=self.config)

        self.supervisor = create_supervisor(
            agents=[self.email_agent.get_agent(), self.calendar_agent.get_agent()],
            model =self.llm,
            output_mode = "full_history", # "full_history give the full history of the conversation, "last_message" gives only the last message
            prompt = self.config["supervisor_prompt"]

        ).compile()


    def get_compiled_supervisor(self):
        return self.supervisor
    



if __name__ == "__main__":
    supervisor = Supervisor()
    compiled_supervisor = supervisor.get_compiled_supervisor()



    query = "Use available tools to schedule a meeting with John Doe on 2023-10-01 at 9:00 AM and then warn him by email"

    # Test it out
    for step in compiled_supervisor.stream(
        {"messages": query},
        stream_mode="updates",
    ):
        for _, update in step.items():
                if update is not None:
                    for message in update.get("messages", []):
                        message.pretty_print()
                        
                    

    