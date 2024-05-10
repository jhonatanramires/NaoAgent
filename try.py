from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from tools import tools

prompt = hub.pull("hwchase17/openai-tools-agent")
print(prompt.input_variables)

# Choose the LLM to use
llm = OllamaFunctions(model="tinyllama")

# Construct the ReAct agent
agent = create_react_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(
  agent=agent, 
  tools=tools, 
  verbose=True,
  return_intermediate_steps=True,
  handle_parsing_errors=True
)

result = agent_executor.invoke({"input": "what is the length of the word \"hello\"?","tools": tools,"tool_names": tools})
print(result.output)
