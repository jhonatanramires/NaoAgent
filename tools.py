# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
import openmeteo_requests
import requests

openmeteo = openmeteo_requests.Client()

@tool
def getWeather(a: str) -> str:
  """
    let you get the current temperature and time really usefull when you need figure out the wheater, temperature and related topics
  """
  url = "https://api.open-meteo.com/v1/forecast"
  params = {
    "latitude": 7.08471,
    "longitude": -70.75908,
    "current": "temperature_2m",
    "forecast_days": 1
  }
  responses = openmeteo.weather_api(url, params=params)
  response = responses[0]
  current = response.Current()
  current_temperature_2m = current.Variables(0).Value()
  return f"the current temperature in Arauca Capital is {current_temperature_2m}°C " + f"and the current time is {current.Time()}"

@tool
def add(a: int) -> int:
    """Adds a and b.

    Args:
      a: first int,
      b: second int
    """
    return int(a) + 4

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

class WordInput(BaseModel):
    word: str = Field(description="should be a single word for find his length")

@tool("get_word_length", args_schema=WordInput, return_direct=False)
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

tools=[add,multiply,getWeather]

#str = ""
#for name in list(tools.keys()):
#  str += (name + ", ") 

#tools_name = str

