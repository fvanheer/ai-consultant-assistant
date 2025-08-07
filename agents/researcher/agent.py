import os

from google.adk.agents import Agent
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search

from researcher.prompts import researcher_prompt

researcher_agent = Agent(
    name="researcher",
    description="A researcher agent that can answer questions about the user's document",
    instruction=researcher_prompt(),
    model=os.getenv("ROOT_AGENT_MODEL"),
    tools=[google_search]
)

root_agent = researcher_agent