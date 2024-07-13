import requests
import json

BASE_URL = 'https://api.mumbaiflood.in/db/'
Monitor = 'https://monitor.mumbaiflood.in/'


def awsstation():
    url = BASE_URL + 'awsstations/'
    response = requests.get(url)
    return response.json()

def stationdata(data):
    url = BASE_URL + 'stationdata/'
    print(data)
    response = requests.post(url, data)
    return response.json()

def awsquaterdata(data):
    url = BASE_URL + 'awsdataforquater/'
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

def updatetrainstation():
    url = BASE_URL + 'updatetrainstation/'
    response = requests.get(url)
    return response.json()

def tweetdata(data):
    url = BASE_URL + 'tweet/'
    response = requests.post(url, data)
    return response.json()

def log(data):
    try:
        url = Monitor + 'logs/'
        response = requests.post(url, data)
        return response.json()
    except Exception as e:
        print(e)
        return None

def systemlog(data):
    url = Monitor + 'systemlog/'
    response = requests.post(url, data)
    return response.json()