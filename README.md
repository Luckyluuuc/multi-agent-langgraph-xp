# README

## How to Run the Code

Make sure you have cloned the project and installed the dependencies using Poetry.

```bash
poetry install
```

Then, you can run the code in two ways:

### LangGraph Studio

LangGraph Studio is a tool that allows you to visualize and run LangGraph architectures. It is a great tool for understanding how the architecture works and for testing it. However, it is a relatively new tool, so it may not be very stable yet. It is still in beta, and some features may be unavailable or lack documentation, but it is a promising tool.

If you want to run it with LangGraph Studio (locally), use the following command:

```bash
poetry run langgraph dev
```

Note: For LangGraph Studio, the important file is `langgraph.json`, which contains the compiled graph objects to visualize and run the architecture. This is why, in the file `src/compiled_graph.py`, we have a collection of objects that are compiled LangGraph graph objects.

### Running the Code in the Shell

You can run the parts you want as usual for Python scripts. For example:

```bash
poetry run python src/your_script.py
```

### Troubleshooting

In case Python cannot find your other modules/packages, run the following command in the shell:

```bash
$env:PYTHONPATH="$pwd/src"
```


## Motivation for this project 

This project investigates the capabilities of LangGraph, particularly focusing on the recent functionalities introduced for constructing architectures that facilitate tool usage within a multi-agent framework.

To demonstrate this, we created a scenario featuring agents that can utilize tools for tasks such as sending emails, searching for the correct email addresses, checking availability, and scheduling meetings. Additionally, the agents manage long-term memory, allowing them to store and retrieve pertinent information.

(Note: Not all tools are utilized in every scenario, and all tools are simulated, For example, the email agent does not send real emails but simulates the process and log the email in a file)



## Multi agent architecture
One of the motivations for this project was to explore the various multi-agent architectures that can be developed using LangGraph, particularly the swarm agent architecture and the supervisor architecture.

For this purpose, we created several reactive agents that collaborate to accomplish tasks:

- An email agent that can send emails and search for a person's email address based on their name.
- A calendar agent that checks user availability and schedules meetings.
- A memory agent that stores and retrieves information from long-term memory.



The key question is: how do we enable these agents to work together?

### Swarm Agent Architecture
In the swarm agent architecture, each agent possesses specific tools (handoff tools) that allow them to transfer conversations to other agents equipped to provide the appropriate responses. There is no hierarchical structure; each agent can seek assistance from others if it lacks the necessary tools to address a user query.

You can find this architecture in the ``swarm_agent`` package/folder, with the final structure available in the ``swarm_agent_orchestration.py`` file, which you can execute.

![Graph swarm](/attachements/2025-04-10-graph%20swarm.png)

### Supervisor Agent Architecture

In the supervisor agent architecture, a supervisor agent oversees the conversation and assigns tasks to other agents. This architecture is more hierarchical, with the supervisor agent managing the overall process and delegating tasks to specialized agents.

Each sub-agent can only communicate with the supervisor agent, which then coordinates the conversation and ensures that the appropriate agents are involved in the process.

You can find this architecture in the `supervisor_agent` package/folder, with the final structure available in the `supervisor_agent_orchestration.py` file, which you can execute.

(Note: For simplicity , the memory agent is not used here, but it can be easily integrated.)

![Graph supervisor](/attachements/2025-04-10-graph%20supervisor.png)


## Miscellaneous Functionality

In this section, we will present additional functionalities that are not directly related to the multi-agent architecture but are interesting to explore, provided by LangGraph or related libraries.


### BigTools

BigTools is not strictly a multi-agent architecture, but it addresses a similar challenge: how to effectively utilize a large number of tools without overloading a single agent's context window, which can lead to increased susceptibility to hallucinations. 

The concept is quite elegant: we first perform a retrieval-augmented generation to identify the k most relevant tools based on the user query. We then present only these k tools to the agent and instruct it to use them. This approach allows for the utilization of multiple tools within a single agent without overwhelming its context window.

You can find this architecture in the `bigtools` package/folder, with the final structure available in the `big_tool_agent.py` file, which you can execute.

(Note: Although this architecture is displayed in LangGraph Studio for visualization purposes, it cannot be used within the studio because I did not find how to pass a custom store, which is necessary for storing the tools and their embeddings. Therefore, it can only be utilized in a script.)

![Graph bigtools](/attachements/2025-04-10-graph%20bigtools.png)
### Memory Agent

We mentioned this agent in the previous sections, but it is interesting in its own. To manage what is referred to in the literature as long-term memory (specifically long-term semantic memory, meaning we only store facts), we can utilize a store and incorporate specific tools that enable us to store and retrieve information from this store. 

For example, we can instruct the agent to remember a fact and later ask it to recall that fact.

To see how this works, you can check the `memory_agent.py` file in the `swarm_agent` package and the tools located in the `tools/tools` directory.


### Self improving agent (procedural memory)

One capability that is both exciting and somewhat daunting is the ability to create agents that can improve themselves. This is referred to in the literature as procedural long-term memory. The idea is that the agent can learn from feedback and modify its system prompt, thereby changing its behavior.

To achieve this, LangGraph provides libraries that can be used to create self-improving agents. We experimented with this on a single agent (the email agent), starting with a simple prompt. For example, when we asked the agent to send an email, then we provided feedback to always sign the email with my name, "Luc." The agent then updated its system prompt to include this information, ensuring that it would always sign emails with "Luc" in the future.

While we did not test it here, LangGraph also offers the ability to optimize multiple prompts simultaneously, using a system that selects which prompts to optimize based on feedback.

(Note: In this experiment, the prompt optimization was quite slow.)

You can find traces of this experiment in the `src/procedural_memory` folder.

### Testing Our Agents

Given that the autonomous nature of agents can lead to unexpected behavior, it is crucial to test them to ensure they function as intended. The `agentEval` library provides a framework for testing agents.

This library allows us to create tests that compare the output of the model against a reference output for a given input by looking at what tools are used, in what order, and what the final output is. Depending on how we define our tests, we can determine whether the agent passes the evaluation.

You can find a simple test (just for me to try this librairy) of the email agent in the `tests/eval_email.py` file
