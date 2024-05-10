import os 

os.environ["FIREWORKS_API_KEY"] = "vKWWWR4PYRAw1gSGL2OIA7SAQYAlMTRiyF6l7k6R0GnOoyox"

from langchain_fireworks import Fireworks 

llm = Fireworks(
    api_key="vKWWWR4PYRAw1gSGL2OIA7SAQYAlMTRiyF6l7k6R0GnOoyox",
    model="accounts/fireworks/models/mixtral-8x7b-instruct",
    max_tokens=256
)
llm("Name 3 sports.")