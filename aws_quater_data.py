import requests
import logging
from connections import awsstation, awsquaterdata


def fetch_aws_data(station_id):
    url = "https://dmwebtwo.mcgm.gov.in/api/tabWeatherForecastData/loadById"
    headers = {
        "Authorization": "Basic RE1BUElVU0VSOkRNYXBpdXNlclBhJCR3b3JkQDEyMzQ="
    }
    payload = {"id": station_id}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return parse_data(data)
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data for station {station_id}: {e}")
        return

def parse_data(data):
    dummy_data = data.get('dummyTestRaingaugeDataDetails', {})
    print(dummy_data)
    
    result = {
        # 'temp_out': parse_value(dummy_data.get('tempOut')),
        # 'out_humidity': parse_value(dummy_data.get('outHumidity')),
        # 'wind_speed': parse_value(dummy_data.get('windSpeed')),
        'rain': parse_value(dummy_data.get('rain')),
    }
    return result

def parse_value(value):
    if value is None or value == '---':
        return None
    try:
        return float(value)
    except ValueError:
        logging.error(f"Failed to parse value '{value}' as float.")
        return None


def fetch_and_store_quater_data():
    stations = awsstation()
    for station in stations: 
        data = fetch_aws_data(station['station_id'])
        if data:
            save_station_data(station, data)

def save_station_data(station, data):
    rainfall = data.get('rain', 0)

    awsquaterdata(
        {
            'station': station['station_id'],
            'rainfall': rainfall
        }
    )
    