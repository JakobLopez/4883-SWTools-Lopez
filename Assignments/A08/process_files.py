"""
Course: cmps 4883
Assignemt: A08
Date: 3/30/19
Github username: JakobLopez
Repo url: https://github.com/JakobLopez/4883-SWTools-Lopez
Name: Jakob Lopez
Description: 
    
"""
import json
import os,sys


"""
Name: is_json
Description: 
    Determines if data from file is JSON
Params:
    myjson - data read from a JSON file
Returns:
    true if file is JSON, false otherwise 
"""
def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


"""
Name: openFileJson
Description: 
    Opens file for reading.
    Convert JSON file to dictionary.
    Errors if path is not JSON.
Params:
    path - path to a JSON file
Returns:
    Dictionary if path is JSON
"""
def openFileJson(path):
    try:
      f = open(path, 'r')
      data = f.read()
      if is_json(data):
          return json.loads(data)
      else:
          print('Error: Not json.')
          return {}
    except IOError:
        print('Error: Game file doesn\'t exist.')
        return {}
