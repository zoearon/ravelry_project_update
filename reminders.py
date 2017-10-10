import schedule
import time
from twilio.rest import Client
import os

def send_message():

    print "git commit"


def send_text():


    # Your Account SID from twilio.com/console
    account_sid = os.environ['TWILIO_SID']
    # Your Auth Token frpm twilio.com/console
    auth_token  = os.environ['TWILIO_TOKEN']

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=os.environ['MY_PHONE'], 
        from_=os.environ['TWILIO_NUM'],
        body="Hello from Python!")

    print(message.sid)

def message():
    """ Create mesage from database info """

    update_freqs = db.session.query(User.update_time, Project).join(
                                   Project).filter(Project.status_id == 1,
                                                   Project.updated_at < (
                                                    now - datetime.timedelta(days=User.update_time))).all()

    mess = "%s projects haven't been updated in %s days!" % count, freq
# schedule.every().day.at("10:30").do(send_message)
schedule.every(15).minutes.do(send_text)

if __name__ == "__main__":
    while True:
        schedule.run_all()
        time.sleep(1)