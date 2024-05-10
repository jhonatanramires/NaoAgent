from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent
from langchain.agents import AgentExecutor

class AgentHandler():
    def __init__(self,temperature,tools,agent_context,openai_api_key):
        #charge llm and format the system_message
        self.llm = ChatOpenAI(temperature=0,openai_api_key=openai_api_key)
        self.tools = tools
        system_message = SystemMessage(content=agent_context)
        prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)
        
        # construct OpenAIFunctionAgent
        self.agent = OpenAIFunctionsAgent(llm=self.llm, tools=self.tools, prompt=prompt)
        
        #  creating agent executor
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

    def run(self,prompt):
        return self.agent_executor.run(prompt)