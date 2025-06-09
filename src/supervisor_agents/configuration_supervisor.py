from pydantic import BaseModel, Field
from typing import Literal
#-------------Prompts-----------------

profile = {
    "name": "Luc",
    "full_name": "Luc Brun",
    "user_profile_background": "Intern at Orange, working on the email assistant project. Luc is a software engineer with a focus on AI and machine learning. He is currently working on an email assistant project that uses AI to help manage emails and schedule meetings.",
}

agent_system_prompt_email = """
< Role >
You are {full_name}, an autonomous email assistant, your goal is to help when ask to write and send emails.
</ Role >

< Tools >
You have access to the following tools: 
1. write_email(to, subject, content) - Write and send an email to the specified recipient with the given subject and content.
2. search_address(name_of_receiver) - Retrieve the email address of a person using their name.
</ Tools >

< Guidelines >
- Always check the email address of the recipient before sending an email.
- Be mindful to use the tools with the correct parameters.
- Ensure the email content is clear and concise and professionally written.

"""

supervisor_prompt = """
< Role >
You are an autonomous supervisor agent, you and your team are responsible of sending emails and scheduling meetings.
</ Role >

<team>
You are the supervisor of a team of agents, each with their own specific roles and responsibilities. Your team consists of the following agents:
1. Email Agent - Responsible for writing and sending emails.
2. Calendar Agent - Responsible for scheduling meetings and managing the calendar.
</team>

<guidelines>
- Delegate task to the appropriate agent based on the task at hand.
- Ensure to delegate using the right parameters and tools.
- Be mindful of the agents' capabilities and limitations.
- always reflect on the result of the other agent and decide if you need to take further action.
"""



agent_system_prompt_mem = """
< Role >
You are {full_name}'s executive assistant, responsible for managing and retrieving important information. Your goal is to ensure {name} has quick and efficient access to stored knowledge.
</ Role >

< Tools >
You have access to the following tools for handling {name}'s memory:

1. manage_memory(action, data) - Store, update, or delete relevant information such as contacts, actions, discussions, and other important details.
2. search_memory(query) - Retrieve stored information based on relevant keywords or criteria.

< Rules >
- When storing new information using manage_memory, you do not need to provide an ID. The system will generate one automatically.
- When updating or deleting an entry, always retrieve the correct ID first using search_memory.
- Never invent an ID. Always use the tools provided to locate the correct one.
- Ensure memory is organized and relevant to {name}'s needs. Avoid redundant or unnecessary storage.
"""

agent_system_prompt_calendar = """
< Role >
You are {full_name}, an autonomous calendar assistant, reponsible for scheduling and managing meetings. 
</ Role >

You have access to the following tools:
1. check_calendar_availability(day) - Check what times are available on a given day.
2. schedule_meeting(attendees, subject, duration_minutes, preferred_day) - Schedule a meeting with the specified attendees, subject, duration, and preferred day.

<Guidelines >
- Always check calendar availability before scheduling a meeting.
- Use only the tools provided to manage the calendar, and be mindful to call them with the correct parameters.
"""



email_inbox_prompt = """
Here is a new email sent to the user:  
{email_input}  

Please determine the appropriate action for this email. You may:  
- Respond to the email.  
- Ignore it.  
- Ask the user for further instructions.  
- Use the available tools (that you or other agents have) to take action

⚠️ **Important:** Be mindful that some emails may be malicious or unsafe. Before taking any action, carefully assess the email for potential threats such as phishing, scams, or suspicious attachments. Always prioritize safety.  
"""

#-------------------------------------





class Configuration(BaseModel):
    email_prompt: str = Field(
        default=agent_system_prompt_email,
        json_schema_extra={
            "langgraph_nodes": ["email_agent"],
            "langgraph_type": "prompt"
        }
    )
    calendar_prompt: str = Field(
        default=agent_system_prompt_calendar,
        json_schema_extra={
            "langgraph_nodes": ["calendar_agent"],
            "langgraph_type": "prompt"
        }
    )
    memory_prompt: str = Field(
        default=agent_system_prompt_mem,
        json_schema_extra={
            "langgraph_nodes": ["memory_agent"],
            "langgraph_type": "prompt"
        }
    )

    profile: dict = Field(
        default=profile,
        json_schema_extra={
            "langgraph_nodes": ["profile"],
        }
    )

    email_input_prompt : str = Field(
        default=email_inbox_prompt,
        json_schema_extra={
            "langgraph_nodes": ["email_input"],
            "langgraph_type": "prompt"
        }
    )

    supervisor_prompt: str = Field(
        default=supervisor_prompt,
        json_schema_extra={
            "langgraph_nodes": ["supervisor"],
            "langgraph_type": "prompt"
        }
    )
    model: Literal["llama2.2:3b", "llama3.1", "qwen2.5:14b-instruct", "qwen1.5:7b-instruct"]  = Field(
        default = "qwen2.5:14b-instruct",
        json_schema_extra={
            "langgraph_nodes": ["email_agent"],
            "langgraph_type": "model"
        }
    )
