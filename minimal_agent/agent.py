from google.adk.agents import LlmAgent
from . import prompts
from . import tools

# Define the agent
root_agent = LlmAgent(
    name="minimal_agent",
    model="gemini-1.5-flash", # Using a common, fast model
    instruction=prompts.INSTRUCTION,
    tools=[tools.simple_tool],
)
