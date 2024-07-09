from tweetparser import tweetpipeline
import schedule
import time
from connections import log, systemlog

def every_hour():
    try :
        tweetpipeline()
        log({
            'log_text' : 'tweets saved',
            'priority' : 1
        })

    except Exception as e:
        try :
            log ({
                'log_text' : 'tweets save failed',
                'priority' : 2
            })
        except Exception as e:  
            print (e)

def system_log():
    try :
        systemlog({'code':'Tweets'})
    except Exception as e:
        print (e)

schedule.every().hour.at(":5").do(every_hour)
schedule.every().minute.do(system_log)

while True:
    schedule.run_pending()
    time.sleep(1)