from connections import awsstation, stationdata


for data in awsstation():
    # fetch id from dict
    station_id = data['station_id']
    print("Fetching data for station", station_id)
