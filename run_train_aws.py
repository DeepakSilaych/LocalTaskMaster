from aws_quater_data import fetch_and_store_quater_data
from connections import log, systemlog, updatetrainstation

import schedule
import time


def every_15_min():
    try :
        fetch_and_store_quater_data()
        log({
            'log_text' : '15 min rainfall data Saved',
            'priority' : 0
        })

    except Exception as e:
        log ({
            'log_text' : '15 min rainfall data not saved ' + str(e),
            'priority' : 1
        })
    
    try :
        updatetrainstation()
    except Exception as e:
        log ({
            'log_text' : 'Train Station Update Failed ' + str(e),
            'priority' : 1
        })


def system_log():
    try :
        systemlog({'code':'AWS Stationss'})
    except Exception as e:
        print (e)
    

schedule.every().hour.at(":00").do(every_15_min)
schedule.every().hour.at(":15").do(every_15_min)
schedule.every().hour.at(":30").do(every_15_min)
schedule.every().hour.at(":45").do(every_15_min)
schedule.every().minute.do(system_log)

while True:
    schedule.run_pending()
    time.sleep(1)