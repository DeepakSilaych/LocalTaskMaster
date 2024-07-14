from hourlyprediction import predict_hourly
import schedule
import time
from connections import log, systemlog



def every_hour():
    try :
        predict_hourly()
        log({
            'log_text' : 'Hourly Prediction Done',
            'priority' : 0
        })

    except Exception as e:
        log ({
            'log_text' : 'Hourly Prediction Failed ' + str(e),
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