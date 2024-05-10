from langchain import hub
from langchain.agents import AgentExecutor, create_xml_agent
from langchain_community.llms import Ollama
from langchain.memory import ChatMessageHistory
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
import bs4
from tool import tools
import sys

prompt = hub.pull("richard-park/xml-agent-convo")

llm = Ollama(model="gemma:2b")

agent = create_xml_agent(llm, tools, prompt)

history = ChatMessageHistory()

history.add_ai_message("i am Nao an assistant that use tools")


# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(
  agent=agent, 
  tools=tools, 
  verbose=True,
  return_intermediate_steps=True
)

print(sys.argv[1])

input = str(sys.argv[1])

res = agent_executor.invoke({
  "input": input,
  "chat_history": history.messages
})

#print(res)
#print("///////////////////////////////////////////////////////////////////////////////////////")
print(res['output'])