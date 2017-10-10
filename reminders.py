import schedule
import time
from twilio.rest import Client
import os
import datetime
from server import app
from model import connect_to_db, db, User, Project, Status, Image

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

    now = datetime.datetime.now()
    update_freqs = db.session.query(User.update_time, Project).join(
                                   Project).filter(Project.status_id == 1,
                                                   Project.updated_at < (
                                                    now - datetime.timedelta(days=14))).all()

    freq = update_freqs[0][0]
    count = len(update_freqs)
    mess = "%s projects haven't been updated in %s days!" % (count, freq)

    print mess
# schedule.every().day.at("10:30").do(send_message)
schedule.every(15).minutes.do(send_text)

if __name__ == "__main__":
    # while True:
    #     schedule.run_all()
    #     time.sleep(1)

    connect_to_db(app)
    message()