from langchain_core.tools import tool
from langmem import create_manage_memory_tool, create_search_memory_tool
from langgraph_swarm import create_handoff_tool

import os
from datetime import datetime


# Files to put together all the tools

#------------E mail Tools------------------
@tool
def write_email(to: str, subject: str, content: str) -> str:
    """Write, send, and log an email."""
    # Placeholder response - in real app would send email
    send_result = f"Email sent to {to} with subject '{subject}'"
    
    # Log the email
    log_result = log_email(to, subject, content)
    
    return f"{send_result}" #\n{log_result}"

def log_email(to: str, subject: str, content: str) -> str:
    """Log the email in a file within the 'emails' folder."""
    # Create 'emails' folder if it doesn't exist
    email_folder = "emails_and_meetings"
    os.makedirs(email_folder, exist_ok=True)
    
    # Generate a unique filename based on timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{email_folder}/{timestamp}_email_{subject}.txt"
    
    # Write email content to the file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"To: {to}\n")
        f.write(f"Subject: {subject}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("\n")  # Blank line to separate headers from content
        f.write(content)
    
    return f"Email logged in file: {filename}"



@tool
def search_address(name_of_receiver: str) -> str:
    """Retrieve email address of a person using his name."""
    # Placeholder response - in a real application, this would remove the email from the inbox
    return f"{name_of_receiver}@gmail.com"



#------------Calendar Tools------------------
@tool
def schedule_meeting(
    attendees: list[str], 
    subject: str, 
    duration_minutes: int, 
    preferred_day: str
) -> str:
    """Schedule a calendar meeting and log it."""
    # Placeholder response - in real app would check calendar and schedule
    schedule_result = f"Meeting '{subject}' scheduled for {preferred_day} with {len(attendees)} attendees"
    
    # Log the meeting
    log_result = log_meeting(attendees, subject, duration_minutes, preferred_day)
    
    return f"{schedule_result}" #\n{log_result}"

def log_meeting(
    attendees: list[str], 
    subject: str, 
    duration_minutes: int, 
    preferred_day: str
) -> str:
    """Log the meeting in a file within the 'meetings' folder."""
    # Create 'meetings' folder if it doesn't exist
    meetings_folder = "emails_and_meetings"
    os.makedirs(meetings_folder, exist_ok=True)
    
    # Generate a unique filename based on timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{meetings_folder}/{timestamp}_meeting_{subject}.txt"

    
    # Write meeting details to the file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Subject: {subject}\n")
        f.write(f"Preferred Day: {preferred_day}\n")
        f.write(f"Duration (minutes): {duration_minutes}\n")
        f.write(f"Date Logged: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("\n")  # Blank line to separate headers from attendees list
        f.write("Attendees:\n")
        for attendee in attendees:
            f.write(f"- {attendee}\n")
    
    return f"Meeting logged in file: {filename}"

@tool
def check_calendar_availability(day: str) -> str:
    """Check calendar availability for a given day."""
    # Placeholder response - in real app would check actual calendar
    return f"Available times on {day}: 9:00 AM, 2:00 PM, 4:00 PM"

#---------------Memory Tools------------------


manage_memory_tool = create_manage_memory_tool(
    namespace=(
        "semantic_memory",
    )
)

search_memory_tool = create_search_memory_tool(
    namespace=(

        "semantic_memory",
    )
)

#-----------Handoff tool (for swarm architecture)------------------
# :WARNING: The name of the agent is important. It should be the same as the agent name when creating the agent (should be specified even if optional in the agent creation function).
transfer_calendar = create_handoff_tool(agent_name="calendar_agent", description="Transfer to calendar agent for calendar-related tasks, do not use any argument with this tool, the next agent will have access to the history of the conversation.")
transfer_memory = create_handoff_tool(agent_name="memory_agent", description="Transfer to memory agent for memory-related tasks, do not use any argument with this tool, the next agent will have access to the history of the conversation.")
transfer_email = create_handoff_tool(agent_name="email_agent", description="Transfer to email agent for email-related tasks. do not use any argument with this tool, the next agent will have access to the history of the conversation.")

