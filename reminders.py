import schedule
import time
from twilio.rest import Client
import os
import datetime
from server import app
from model import connect_to_db, db, User, Project, Status, Image

def send_message():

    print "git commit"


def send_text(recipient=os.environ['MY_PHONE'], text):


    # Your Account SID from twilio.com/console
    account_sid = os.environ['TWILIO_SID']
    # Your Auth Token frpm twilio.com/console
    auth_token  = os.environ['TWILIO_TOKEN']

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=recipient, 
        from_=os.environ['TWILIO_NUM'],
        body=text)

    print(message.sid)

def message():
    """ Create mesage from database info """

    now = datetime.datetime.now()

    users = db.session.query(User.user_id, User.update_date, User.phone_num).filter(User.subscribed).all()
    
    for user in users:
        user_id, freqency, phone = user
        update_count = db.session.query(Project).filter(Project.status_id == 1,
                                                        Project.user_id == user_id,
                                                       Project.updated_at < (
                                                        now - datetime.timedelta(days=freqency))).count()
        body = format_message(update_count, freqency)

        print body
        
        send_text(phone, body)


def format_message(count, freqency):
    """ write the text for each user who is subsribed """

    text = "%s projects haven't been updated in %s days!" % (count, freqency)
    return text


# schedule.every().day.at("10:30").do(send_message)
# schedule.every(15).minutes.do(send_text)

if __name__ == "__main__":
    # while True:
    #     schedule.run_all()
    #     time.sleep(1)

    connect_to_db(app)
    message()