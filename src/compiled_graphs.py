### This file is used to get the compiled graph that we want to display in the langgraph studio UI


from src.agents.email_agent import EmailAgent
from src.agents.memory_agent import MemoryAgent
from src.agents.calendar_agent import CalendarAgent
from src.supervisor_agents.configuration_supervisor import Configuration
from src.supervisor_agents.supervisor_architecture_orchestration import Supervisor
from langgraph.store.memory import InMemoryStore

from src.swarm_agents.swarm_agent_orchestration import Swarm
from model.embedding import Embddings
from bigtool_agent.bigtool_agent import bigtool_agent # This is not unused, if you want to use langgraph studio for visualization, you need to import this
from model.model import Model



swarm_graph = Swarm().get_compiled_swarm()
supervisor_graph = Supervisor().get_compiled_supervisor()

config = Configuration()
llm = Model(name="qwen2.5:7b-instruct", local=True).initialize_and_get_model()
email_agent = EmailAgent(llm=llm, config=config).get_agent()
calendar_agent = CalendarAgent(llm=llm, config=config).get_agent()


embeddings = Embddings().get_embedding_obj()
memory_agent = MemoryAgent(llm=llm, config=config).get_agent()



