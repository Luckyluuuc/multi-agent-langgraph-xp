import json
from agentevals.trajectory.match import create_trajectory_match_evaluator
from agentevals.trajectory.llm import create_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT # not used here because llm as a judge requires openAI, does not work with ollama
from src.supervisor_agents.configuration_supervisor import Configuration
from src.agents.email_agent import EmailAgent
from src.model.model import Model
from langchain_core.messages import convert_to_openai_messages

# Constants for reusability and clarity
USER_QUERY = "Please send an email to Bob to tell him thanks for his help this morning."
REFERENCE_TRAJECTORY = [
    {
        'role': 'user',
        'content': 'Please send an email to Alice to tell him thanks for his help this morning.'
    },
    {
        'role': 'assistant',
        'name': 'email_agent',
        'tool_calls': [
            {
                'type': 'function',
                'id': '6e02803f-74c9-4eea-959a-980b9f4a10b6',
                'function': {
                    'name': 'search_address',
                    'arguments': '{"name_of_receiver": "Alice"}'
                }
            }
        ],
        'content': ''
    },
    {
        'role': 'tool',
        'name': 'search_address',
        'tool_call_id': '6e02803f-74c9-4eea-959a-980b9f4a10b6',
        'content': 'Alice@gmail.com'
    },
    {
        'role': 'assistant',
        'name': 'email_agent',
        'tool_calls': [
            {
                'type': 'function',
                'id': 'a6067bce-1de1-46bb-9139-7d7aa2e0d726',
                'function': {
                    'name': 'write_email',
                    'arguments': (
                        '{"content": "Thank you for your help this morning, Alice.", '
                        '"subject": "Thank You", '
                        '"to": "Alice@gmail.com"}'
                    )
                }
            }
        ],
        'content': ''
    },
    {
        'role': 'tool',
        'name': 'write_email',
        'tool_call_id': 'a6067bce-1de1-46bb-9139-7d7aa2e0d726',
        'content': "Email sent to Alice@gmail.com with subject 'Thank You'"
    },
    {
        'role': 'assistant',
        'name': 'email_agent',
        'content': (
            "The email has been sent to Alice thanking him for his assistance this morning."
        )
    }
]

# Step 1: Initialize Configuration and Model
config = Configuration()
model = Model(name="qwen2.5:14b-instruct", local=True).initialize_and_get_model()

# Step 2: Create Email Agent
email_agent = EmailAgent(llm=model, config=config).get_agent()

# Step 3: Invoke Email Agent with User Query
try:
    response = email_agent.invoke(
        {"messages": [{"role": "user", "content": USER_QUERY}]}
    )
    
    # Validate response structure
    if "messages" not in response:
        raise ValueError("Invalid response format from email agent.")
    
    # Convert response messages to OpenAI format
    output_messages = convert_to_openai_messages(response["messages"])
except Exception as e:
    print(f"Error during agent invocation: {e}")
    output_messages = []

# Step 4: Create Trajectory Evaluator
trajectory_evaluator = create_trajectory_match_evaluator(
    trajectory_match_mode="strict",  # Strict mode ensures exact match of trajectories
    tool_args_match_mode="ignore"   # Ignore tool argument differences for evaluation because we are not interested in the content of the mail for example
)

# Step 5: Evaluate Trajectory Match
try:
    trajectory_result = trajectory_evaluator(
        outputs=output_messages,
        reference_outputs=REFERENCE_TRAJECTORY,
    )
    
    # Print the evaluation result in a readable JSON format
    print("Trajectory result:")
    print(json.dumps(trajectory_result, indent=2))
except Exception as e:
    print(f"Error during trajectory evaluation: {e}")
