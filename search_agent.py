import logging

from deepagents import create_deep_agent
from langchain_google_genai import ChatGoogleGenerativeAI

# Silence harmless google-genai warnings (AFC notice, unsupported schema keys)
logging.getLogger("google_genai.models").setLevel(logging.ERROR)
logging.getLogger("google_genai._common").setLevel(logging.ERROR)

# System prompt to steer the agent to be an expert researcher
research_instructions = """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. It returns a grounded summary of the search results along with source URLs.
"""

# Gemini rejects built-in tools (like google_search) mixed with the function tools
# deepagents adds, so run the grounded search in a separate model call.
search_model = ChatGoogleGenerativeAI(model="gemini-3.6-flash").bind_tools([{"google_search": {}}])


def internet_search(query: str) -> str:
	"""Search the internet with Google Search and return a summary of the results with sources."""
	response = search_model.invoke(query)
	sources = [
		f"- {chunk['web']['title']}: {chunk['web']['uri']}"
		for chunk in response.response_metadata.get("grounding_metadata", {}).get("grounding_chunks", [])
		if chunk.get("web")
	]
	return response.text + ("\n\nSources:\n" + "\n".join(sources) if sources else "")


agent = create_deep_agent(
	model="google_genai:gemini-3.6-flash",
	tools=[internet_search],
	system_prompt=research_instructions
)

result = agent.invoke({"messages": [{"role": "user", "content": "What is langgraph?"}]})
print(result["messages"][-1].text)
