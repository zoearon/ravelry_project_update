
import datetime
from model import db, User, Image
import requests
import os
from PIL import Image as pilImage

def time_difference_now(time):
    """ Find how much time has passed since a datetime in days"""

    NOW = datetime.datetime.now()

    diff = NOW - time

    # day_seconds = diff.seconds/(24.00 * 60 * 60.00)

    # days = diff.days + day_seconds

    return diff.days


def sort_projects_by_update(projects):
    """ sort a list of project objects into 2 lists based on update """

    need_update = []
    update = []

    for project in projects:
        since_update = time_difference_now(project.updated_at)
        if since_update > 14:
            need_update.append((project, since_update))
        else:
            update.append((project, since_update))

    return need_update, update


def check_username(user):
    """ check if a user is in the database """

    # active_user = User.query.filter_by(username = user).first()

    # if active_user:
    #     flash( "Login Successful")
    #     session['user'] = active_user.user_id
    # else:
    #     flash("Login Failed")


def post_project_db_update(project, notes, status, image, user):
    """ update a project in the db and ravelry site """

    project.notes = notes
    project.status_id = int(status)
    project.updated_at = datetime.datetime.now()
    if image:
        image = Image(url=photo, project_id=project.project_id)
        db.session.add(image)
    db.session.commit()
    