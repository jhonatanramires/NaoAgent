from langchain import hub
from langchain.agents import AgentExecutor, create_xml_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from tools import tools

prompt = hub.pull("richard-park/xml-agent-convo")

llm = ChatOllama(model="gemma:2b")

agent = create_xml_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(
  agent=agent, 
  tools=tools, 
  verbose=True,
  return_intermediate_steps=True,
  handle_parsing_errors=True
)

res = agent_executor.invoke({"input": "what is the temperature and based in that is good doing exercise?"})
print(res)
print("///////////////////////////////////////////////////////////////////////////////////////")
print(res['output'])