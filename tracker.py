
import datetime
from model import db, User, Image
import requests
import os

NOW = datetime.datetime.now()

def time_difference_now(time):
    """ Find how much time has passed since a datetime in days"""


    diff = NOW - time

    day_seconds = diff.seconds/(24.00 * 60 * 60.00)

    days = diff.days + day_seconds

    return days


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

def post_project_update(project, notes, status, image, user):
    """ update a project in the db and ravelry site """

    project.notes = notes
    project.status_id = int(status)
    project.updated_at = NOW
    if image:
        post_add_image(project, user, image)
    db.session.commit()

    data = {"notes": notes, "project_status_id": status}

    response = requests.post("https://api.ravelry.com/projects/%s/%s.json" %
                              (user.username, project.project_id),
                              data,
                              auth=(os.environ['RAVELRY_ACCESS_KEY'],
                                    os.environ['RAVELRY_PERSONAL_KEY']))

def post_add_image(project, user, photo):
    """ add an image to the db and project page """

    image = Image(url=photo, project_id=project.project_id)
    db.session.add(image)

    data = {"source_url": photo}
    response = requests.post("https://api.ravelry.com/projects/%s/%s/create_photo.json" %
                              (user.username, project.project_id),
                              data,
                              auth=(os.environ['RAVELRY_ACCESS_KEY'],
                                    os.environ['RAVELRY_PERSONAL_KEY']))