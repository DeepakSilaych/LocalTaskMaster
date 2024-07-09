from awsdata import fetch_and_store_data
from connections import log, systemlog

import schedule
import time


def every_15_min():
    try :
        # fetch_and_store_data()
        log({
            'log_text' : 'Station Data Saved',
            'priority' : 0
        })

    except Exception as e:
        try :
            log ({
                'log_text' : 'Station Data Save Failed',
                'priority' : 1
            })
        except Exception as e:
            print (e)

def system_log():
    try :
        systemlog({'code':'AWS Stationss'})
    except Exception as e:
        print (e)

schedule.every().hour.at(":0").do(every_15_min)
schedule.every().hour.at(":15").do(every_15_min)
schedule.every().hour.at(":30").do(every_15_min)
schedule.every().hour.at(":45").do(every_15_min)
schedule.every().minute.do(system_log)

while True:
    schedule.run_pending()
    time.sleep(1)