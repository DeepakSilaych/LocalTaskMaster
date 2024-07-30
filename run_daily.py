from daywiseprediction import dailyprediction
from gfs import download_gfs_data
import schedule
import time
from connections import log, systemlog



def every_day():
    try :
        try :
            download_gfs_data()
        except:
            log({
                'log_text' : 'GFS Data Download Failed',
                'priority' : 1
            })
            
        dailyprediction()
        log({
            'log_text' : 'Daily Prediction Done',
            'priority' : 1
        })

    except Exception as e:
        log ({
            'log_text' : 'Daily Prediction Failed' + str(e),
            'priority' : 1
        })
            
def system_log():
    try :
        systemlog({'code':'Daily Forecast'}) 
    except Exception as e:
        print (e)


schedule.every().day.at("16:20").do(every_day)
schedule.every().minute.do(system_log)

every_day()

while True:
    schedule.run_pending()
    time.sleep(1)