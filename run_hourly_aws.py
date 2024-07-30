from aws_hourly_data import fetch_and_store_hourly_data
import schedule
import time
from connections import log, systemlog


def every_hour():
    try :
        fetch_and_store_hourly_data()
        log({
            'log_text' : 'Hourly Rainfall Data Saved',
            'priority' : 0
        })

    except Exception as e:
        log ({
            'log_text' : 'Hourly Rainfall Data Failed ' + str(e),
            'priority' : 1
        })

def system_log():
    try :
        systemlog({'code':'Hourly Forecast'}) 
    except Exception as e:
        print (e)


schedule.every().hour.at(":05").do(every_hour)
schedule.every().minute.do(system_log)

while True:
    schedule.run_pending()
    time.sleep(1)