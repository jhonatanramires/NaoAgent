from langchain.agents import tool
import openmeteo_requests

openmeteo = openmeteo_requests.Client()

#import sys 

#sys.path.append("..\\utils")

#import subprocess

# def postureNao(ip,posture):
#    Nao_command = "python .\\Nao\\setPosture.py --ip " + str(ip) + " " + "--posture " + str(posture)
#    print(Nao_command)
#    process = subprocess.Popen(Nao_command.split(), stdout=subprocess.PIPE)

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
def get_hum_percent(word: str) -> int:
    """Usefull when ask you about the humilty percent"""
    return
    return fetch("http://192.168.43.165/",True)

@tool
def get_hum_percent(word: str) -> int:
    """Usefull when ask you about the humilty percent"""
    return
    return fetch("http://192.168.43.165/",True)

@tool 
def set_posture_to(posture: str) -> str:
    """Usefull function when ask you for take or go to a posture only if the posture is in the following array ["StandInit","SitRelax","StandZero","LyingBelly","LyingBack","Stand","Crouch","Sit"]"""
    return
    postureNao("192.168.43.96",posture)
    
toolsAI = [getWeather]

