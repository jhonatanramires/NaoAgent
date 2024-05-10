# LangChain supports many other chat models. Here, we're using Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from tools import tools,tools_name
import ast

# found: 1234

# supports many more optional parameters. Hover on your `ChatOllama(...)`
# class to view the latest available supported parameters
llm = ChatOllama(model="gemma:2b")
llm.bind(functions=tools)
prompt = ChatPromptTemplate.from_template("you are a usefull assistand that provide a simple json for take a desicion of which tool use based in the message gived by the user and you choose only one tool and that json must be in the format structured with three fields tool_name, reason and the most important tool_inputs that must be another json like this (\"name_of_value\": value, \"name_of_value\": value) the tool_inputs for this respond must be like this {tools_input} like this (\"reason\": you need to give a meningfull reason for the choose that you make, \"tool_name\": the name of the tool that you choose exactly as it is in the tool list\) and about which tool use for every problem in this time you have this tool list {tools_name} and this is the message from the user {input} you need to provide the json and only ONLY the json nothing else this is an example of how you must response \"{example}\" ")

messages = prompt.format_messages(tools_name=tools_name, user_input="i need to multiply 3 and 2")

# using LangChain Expressive Language chain syntax
# learn more about the LCEL on
# /docs/expression_language/why
chain = prompt | llm | StrOutputParser()

# for brevity, response is printed in terminal
# You can use LangServe to deploy your application for
# production
example = """{
  "tool_name": "add",
  "reason": "You need to add 3 and 2"
}"""

res = chain.invoke({"tools_name": tools_name,"input": "i need to multiply 3 and 2 ","example": example})
print(res+"\n\n---------------------------------------------------------------------------------------------------")
tooluwu = ast.literal_eval("{" + res.partition("{")[2].partition("}")[0] + "}")
print(tools[tooluwu['tool_name']](2,3))
