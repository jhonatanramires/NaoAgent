# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
import openmeteo_requests
import requests

openmeteo = openmeteo_requests.Client()

@tool
def search(a: str) -> str:
    """
      useful for search something
    """
    return ""

@tool
def getWeatherData(a: str) -> str:
    """
    Fetches weather data from an API and returns the weather details as a dictionary.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 7.08471,
        "longitude": -70.75908,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "showers", "snowfall"]
    }
    responses = openmeteo.weather_api(url, params=params)
    return responses[0].Current()

@tool
def getTemperature(a: str):
    """
    Returns the temperature at 2 meters height.
    """
    weather_data = getWeatherData("asf")
    return f"Temperature: {weather_data.Variables(0).Value()}°C"

@tool
def getRelativeHumidity(a: str):
    """
    Returns the relative humidity at 2 meters height.
    """
    weather_data = getWeatherData("asdf")
    return f"Relative Humidity: {weather_data.Variables(1).Value()}%"

@tool
def getApparentTemperature(a: str):
    """
    Returns the apparent temperature.
    """
    weather_data = getWeatherData("asf")
    return f"Apparent Temperature: {weather_data.Variables(2).Value()}°C"

@tool
def getDayOrNight(a: str):
    """
    useful when you have a question about whether it is day or night.
    """
    weather_data = getWeatherData("asf")
    day_status = weather_data.Variables(3).Value()
    return "It is currently day." if day_status else "It is currently night."

@tool
def getPrecipitation(a: str):
    """
    Returns the precipitation level.
    """
    weather_data = getWeatherData("asf")
    return f"Precipitation: {weather_data.Variables(4).Value()}mm"

@tool
def getRain(a: str):
    """
    Returns the rain level.
    """
    weather_data = getWeatherData("asf")
    return f"Rain: {weather_data.Variables(5).Value()}mm"

@tool
def getShowers(a: str):
    """
    Returns the showers level.
    """
    weather_data = getWeatherData("asf")
    return f"Showers: {weather_data.Variables(6).Value()}mm"

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

tools=[add,multiply,search,getTemperature,getRelativeHumidity,getApparentTemperature,getDayOrNight,getPrecipitation,getRain,getShowers]
