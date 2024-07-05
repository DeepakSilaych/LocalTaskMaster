from daywiseprediction import daywiseprediction
from gfs import download_gfs_data
from hourlyprediction import predict_hourly
from tweetparser import tweetdata
from awsdata import fetch_and_store_data
import schedule
import time


def every_15_min():
    fetch_and_store_data()
    print("Saved Station Data at:", time.strftime("%D %H:%M:%S"))

def every_hour():
    predict_hourly()
    print("Downloaded GFS Data at:", time.strftime("%D %H:%M:%S"))

def everyday_at_16_05():
    download_gfs_data()
    daywiseprediction()
    print("Daywise Prediction at:", time.strftime("%D %H:%M:%S"))

def everyday_at_11_50():
    tweetdata()
    print("Tweet Data at:", time.strftime("%D %H:%M:%S"))

# task at :00, :15, :30, :45

schedule.every().hour.at(":09").do(every_15_min)
schedule.every().hour.at(":15").do(every_15_min)
schedule.every().hour.at(":30").do(every_15_min)
schedule.every().hour.at(":45").do(every_15_min)
schedule.every().hour.at(":13").do(every_hour)
schedule.every().day.at("16:05").do(everyday_at_16_05)
schedule.every().day.at("11:50").do(everyday_at_11_50)

while True:
    schedule.run_pending()
    time.sleep(1)
