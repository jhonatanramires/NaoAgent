from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_experimental.llms.ollama_functions import OllamaFunctions

prompt = ChatPromptTemplate.from_messages([
  SystemMessagePromptTemplate("You are an assisant to perform chosing which tool use based in the user input"),
  SystemMessagePromptTemplate("You have the following tools: "),
  SystemMessagePromptTemplate("{tools_name}"),
  SystemMessagePromptTemplate("the user gave you this input: "),
  HumanMessagePromptTemplate("{input}"),
])

llm = OllamaFunctions(model="tinyllama")
