from daywiseprediction import dailyprediction
from gfs import download_gfs_data
import schedule
import time
from connections import log, systemlog



def every_hour():
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
        try :
            log ({
                'log_text' : 'Daily Prediction Failed',
                'priority' : 1
            })
        except Exception as e:  
            print (e)
            
def system_log():
    try :
        systemlog({'code':'Daily Forecast'}) 
    except Exception as e:
        print (e)


schedule.every().daily.at("16:20").do(every_hour)
schedule.every().minute.do(system_log)

while True:
    schedule.run_pending()
    time.sleep(1)