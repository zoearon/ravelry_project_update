import schedule
import time

def send_message():

    print "git commit"

# schedule.every().day.at("10:30").do(send_message)
schedule.every(15).minutes.do(send_message)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)