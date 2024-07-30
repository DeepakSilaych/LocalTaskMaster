import requests
from connections import awsstation, awsquaterdata, log


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
        log({
            'message': f"Failed to fetch data for station {station_id}: {e}",
            'level': 1
        })
        return

def parse_data(data):
    dummy_data = data.get('dummyTestRaingaugeDataDetails', {})
    # print(dummy_data)
    
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
    return float(value)


def save_station_data(station, data):
    rainfall = data.get('rain', 0)
    awsquaterdata({
        "station": station['station_id'],
        "rainfall": rainfall
    })

def fetch_and_store_quater_data():
    stations = awsstation()
    for station in stations:
        station_id = station['station_id']
        data = fetch_aws_data(station_id)
        try :
            save_station_data(station, data)
            
        except Exception as e:
            print(e, station_id, data)
            log({
                'message': f"Failed to fetch or store data for station {station_id}: {e}",
                'level': 1
            }) 

fetch_and_store_quater_data()