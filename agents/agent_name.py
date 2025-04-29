from langchain.agents import Tool, initialize_agent, AgentType
from langchain.llms import OpenAI
from tools.common_tools import example_tool  # Import tools as needed

def create_agent():
    llm = OpenAI(temperature=0)
    tools = [example_tool]  # Replace with actual tools relevant to the agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    return agent