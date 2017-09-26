from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Model defintions

class User(db.Model):
    """ User info for a ravelry user """

    __tablename__ = "users"

    # attributes for users
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    profile_img = db.Column(db.String(200))

    def __repr__(self):
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
    started_at = db.Column(db.DateTime)
    finished_at = db.Column(db.DateTime)

    # relationship between tables
    user = db.relationship("User", backref= 'projects')
    status = db.relationship("Status", backref='projects')

    def __repr__(self):
        return "< Project name= %s>" % (self.name)

class Status(db.Model):
    """ Assign a status_id a status name fixed 

    Assures status_id is valid"""

    __tablename__ = "statuses"

    status_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return "<Status status= %s id= %s>" % (self.status, self.status_id)

class Image(db.Model):
    """ An image for a a project. """

    __tablename__ = "images"

    img_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(500), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))

    project = db.relationship("Project", backref= 'images')

    def __repr__(self):
        return "< Image id= %s>" % (self.img_id)


##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///projects'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)



if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."