from deepagents import create_deep_agent


agent = create_deep_agent(
    model="google_genai:gemini-3.6-flash",
    system_prompt="You are a helpful assistant.",
    tools=[search, fetch_url],
    memory=["./AGENTS.md"],
    skills=["./skills/"],
)