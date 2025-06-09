import os
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage
from pydantic import BaseModel, Field




class Model():
    """
    Class to initialize the model and define the parameters of it. Currently simple, but we may add more parameters for the model here like temperature
    """
    def __init__(self, name:str="qwen2.5:14b"):
        """
        name : str : name of the model to use
        local : bool : if we want to use the local model with ollama or not
            --> dont forget to launch the server with "ollama serve" in the cmd and be sure that you downloaded the model


        ret : ChatOllama or ChatOpenAI object

        Warning in this code we act like chatOpenAi and ChatOllama have the same interface, it is usually true but we should be careful
        """
        self.model_name = name
            

    def initialize_and_get_model(self):
        if self.local: 
            try :
                self.llm = ChatOllama(model=self.model_name)
            except Exception as e:
                print("Error while initializing the local model")
                print(e)
        return self.llm



if __name__ == "__main__": # for a few tests 


    config = Model(name="llama3.1", local=True)
    llm = config.initialize_and_get_model()
    print(llm.invoke("hello").content)
