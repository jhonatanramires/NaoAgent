from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.chat_models import ChatOllama
from AgentOllama import AgentHandler
from tool import tools

llm = ChatOllama(model="gemma:2b")

prompt = PromptTemplate(
    template="you are an assistant that need to divide an complex input into multiple doable taks GIVING THE OUTPUT IN THE FORMAT: .\n{format}\nBase on the following user message:\n{query}\n",
    input_variables=["query","format"]
)

chain = prompt | llm

res = chain.invoke({"query": "tell me the weather","format": '["first task","second task"]'}).content
print(res)
actions = res.partition("[")[2].partition("]")[0].partition(",")


nao = AgentHandler(tools)

def AgentCall(prompt):
  result = nao.run(prompt)
  result = result
  print(result)

for i in range(0,len(actions),2):
  print(actions[i])
  AgentCall(actions[i])