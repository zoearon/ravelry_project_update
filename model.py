from flask_sqlalchemy import SQLAlchemy

from passlib.hash import bcrypt
db = SQLAlchemy()


# Model defintions

class User(db.Model):
    """ User info for a ravelry user """

    __tablename__ = "users"

    # attributes for users
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    profile_img = db.Column(db.String(200))
    password = db.Column(db.String(200), nullable=False)
    update_time = db.Column(db.Integer)
    phone_num = db.Column(db.String(15))
    email = db.Column(db.String(100))
    subscribed = db.Column(db.Boolean, nullable=False)
    api_etag = db.Column(db.String(100))

    def __repr__(self):  # pragma: no cover
        return "<User username= %s>" % (self.username)


class Project(db.Model):
    """ A project created by a user """

    __tablename__ = "projects"

    project_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    pattern_name = db.Column(db.Text)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.status_id'))
    updated_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    notes = db.Column(db.Text)
    progress = db.Column(db.Integer)
    rav_page = db.Column(db.String(100))
    started_at = db.Column(db.DateTime)
    finished_at = db.Column(db.DateTime)
    # etag = db.Column(db.String(100))

    # relationship between tables
    user = db.relationship("User", backref='projects')
    status = db.relationship("Status", backref='projects')

    def __repr__(self):  # pragma: no cover
        return "< Project name= %s>" % (self.name)


class Status(db.Model):
    """ Assign a status_id a status name fixed

    Assures status_id is valid"""

    __tablename__ = "statuses"

    status_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), unique=True)

    def __repr__(self):  # pragma: no cover
        return "<Status status= %s id= %s>" % (self.status, self.status_id)


class Image(db.Model):  
    """ An image for a a project. """

    __tablename__ = "images"

    img_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(500), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))

    project = db.relationship("Project", backref='images')

    def __repr__(self):  # pragma: no cover
        return "< Image id= %s>" % (self.img_id)


##############################################################################
# Helper functions
def example_data():
    user = User(username="abc",
                user_id=1,
                password=bcrypt.using(rounds=13).hash("123"),
                subscribed=True,
                api_etag="123abc"
                )
    db.session.add(user)
    project = Project(project_id=1,
                      name="knit hat",
                      pattern_name="basic",
                      status_id=1,
                      updated_at='2012-10-01 00:00:00',
                      user_id=1,
                      notes="just a basic hat",
                      started_at='2014-10-01 00:00:00',
                      )
    db.session.add(project)
    status = Status(status_id=1, status="Test")
    db.session.add(status)
    status_1 = Status(status_id=2, status="Test_update")
    db.session.add(status_1)
    image = Image(url="https://i.vimeocdn.com/portrait/58832_300x300",
                  project_id=1,
                  )
    db.session.add(image)
    try:
        db.session.commit()
    except: # pragma: no cover
        db.session.rollback()

def connect_to_db(app, db_uri="postgresql:///projects"): # pragma: no cover
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)



if __name__ == "__main__":  # pragma: no cover
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
