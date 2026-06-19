import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
rapid_api_key = os.getenv('RAPID_API_KEY')
url = "https://cricket-api-free-data.p.rapidapi.com/cricket-schedule"

headers = {
    "x-rapidapi-key": rapid_api_key,
    "x-rapidapi-host": "cricket-api-free-data.p.rapidapi.com",
    "Content-Type": "application/json",
}

tool_functions = {}
tool_json_list = []
fixtures_response_list=[]


def tool_function_decorator(name):
    def wrapper(func):
        tool_functions[name] = func
        return func
    return wrapper


@tool_function_decorator('get_fixtures')
def get_fixtures():
    response = requests.get(url, headers=headers)
    print(response.json())
    wrapper_response = response_wrapper(response.json())
    return wrapper_response

def response_wrapper(response_dict):
    match_response = response_dict['response']
    text = "Date : " + match_response['schedules'][0]['scheduleAdWrapper']['date'] 
    match_schedule_lst = match_response['schedules'][0]['scheduleAdWrapper']['matchScheduleList']
    for match in match_schedule_lst:
        text = text + '->'
        text = text + " seriesname: " + match['seriesName'] + " -> "

    return text



def build_tool_registry(json_directory=None):
    if json_directory is None:
        json_directory = os.getcwd()
    registry = {}
    try:
        files = os.listdir(json_directory)
    except Exception:
        return registry

    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(json_directory, file)
            try:
                with open(file_path, 'r') as f:
                    tool_data = json.load(f)
                    tool_json_list.append(tool_data)
                    tool_name = tool_data.get('function', {}).get('name')
                    if tool_name in tool_functions:
                        registry[tool_name] = tool_functions[tool_name]
            except Exception:
                
                continue
    return registry





tool_registry = build_tool_registry()


class ToolRegistry:
    def __init__(self):
        self._registry = tool_registry

    def get_tool_registry(self):
        return self._registry


__all__ = ["tool_registry", "ToolRegistry", "get_fixtures","tool_json_list"]
