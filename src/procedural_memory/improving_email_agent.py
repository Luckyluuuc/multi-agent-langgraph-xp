from tools.tools import write_email, search_address
from langgraph.prebuilt import create_react_agent
from model.model import Model

from langgraph.store.memory import InMemoryStore
from langgraph.config import get_store
from langmem import create_prompt_optimizer



class EmailAgent:
    """
    This class creates a react agent that can send emails and search for addresses.
    But more importantly, it can learn from the feedback given by the user by improving its prompt.
    """
    def __init__(self, llm): 
        self.llm = llm
        self.store = InMemoryStore()
        self.store.put(("instructions",), key="agent_instructions", value={"prompt": "Be a good email agent Write good email and search for adresses when needed."})
        self.tools = [write_email, search_address]
        self.agent = create_react_agent(self.llm, self.tools, store=self.store, prompt=self.create_prompt, name="email_agent")
        
        

    def create_prompt(self, state):
        item = self.store.get(("instructions",), key="agent_instructions")
        instructions = item.value["prompt"]
        sys_prompt = {"role": "system", "content": f"## Instructions\n\n{instructions}"}
        return [sys_prompt] + state['messages']


    def get_agent(self):
        return self.agent
    
    def invoke(self, input):
        """
        This function is used to invoke the agent with the input given by the user.
        It will return the output of the agent.
        """
        return self.agent.invoke(input)
    
    def stream(self, input, stream_mode="updates"):
        """
        This function is used to stream the output of the agent.
        It will return the output of the agent.
        """
        return self.agent.stream(input, stream_mode=stream_mode)

    def learning(self, output, feedback): 
        """
        This function is used to learn from the feedback given by the user.
        it use 
        - the feedback given by the user 
        - the output
        - the current prompt (which is stored in the store if it is not a parameter of the function)

        to improve the prompt of the agent.
        """
        optimizer = create_prompt_optimizer(self.llm)
        current_prompt = self.store.get(("instructions",), key="agent_instructions").value["prompt"]
        feedback = {"request": feedback}
        optimizer_result = optimizer.invoke({"prompt": current_prompt, "trajectories": [(output["messages"], feedback)]})
        print("new prompt : ", optimizer_result)
        self.store.put(("instructions",), key="agent_instructions", value={"prompt": optimizer_result})








    

if __name__ == "__main__":
    llm = Model(name="qwen2.5:14b-instruct", local=True).initialize_and_get_model()
    emailagent = EmailAgent(llm=llm)
    

    #lets loop to test and improve the agent
    while True: 
        #get the input from the user
        user_input = input("input : ")
        #get the output from the agent
        # final_output = {}

        # for step in emailagent.stream({"messages": user_input}, stream_mode="updates"):
        #     for _, update in step.items():
        #         if update is not None:
        #             last_update = update
                    
        #             # Agrégation des données dans l'objet final
        #             for key, value in update.items():
        #                 if key not in final_output:
        #                     final_output[key] = value
        #                 else:
        #                     # Si la clé existe déjà, fusionner les nouvelles données
        #                     if isinstance(value, list):
        #                         final_output[key].extend(value)
        #                     elif isinstance(value, dict):
        #                         final_output[key].update(value)

        #             # Optionnel : Affichage des messages au fur et à mesure
        #             for message in update.get("messages", []):
        #                 message.pretty_print()

        # print("last update : ", last_update)
        output = emailagent.invoke({"messages": user_input})
        print("Final response:")
        for m in output['messages']:
            m.pretty_print()
        #get the feedback from the user
        feedback = input("feedback : ")
        #learn from the feedback
        emailagent.learning(output, feedback)
        print("learning done")

    
    