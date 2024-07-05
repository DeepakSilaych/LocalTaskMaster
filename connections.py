import requests
import json

BASE_URL = 'https://api.mumbaiflood.in/db/'
# BASE_URL = 'http://localhost:8000/db/'

def awsstation():
    url = BASE_URL + 'awsstations/'
    response = requests.get(url)
    return response.json()

def stationdata(data):
    url = BASE_URL + 'stationdata/'
    print(data)
    response = requests.post(url, data)
    return response.json()

def fetchstationdata(station):
    url = BASE_URL + 'stationdata/'
    response = requests.get(url, station)
    return response.json()

def daywiseprediction(data):
    url = BASE_URL + 'daywiseprediction/'
    response = requests.post(url, data)
    return response.json()

def hourwiseprediction(data):
    url = BASE_URL + 'hourlyprediction/'
    response = requests.post(url, data)
    return response.json()

def updatetrainstation(data):
    url = BASE_URL + 'updatetrainstation/'
    response = requests.post(url, data)
    return response.json()

def tweetdata(data):
    url = BASE_URL + 'tweet/'
    response = requests.post(url, data)
    return response.json()
