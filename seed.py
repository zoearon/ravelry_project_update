from model import connect_to_db, db, User, Project, Status, Image
import datetime
import requests
import os
import api
from passlib.hash import bcrypt


def load_user():
    """ Add the current user to the database"""

    user_json = requests.get("https://api.ravelry.com/current_user.json",
                             auth=(os.environ['RAVELRY_ACCESS_KEY'],
                                   os.environ['RAVELRY_PERSONAL_KEY'])).json()

    user = user_json['user']

    # check if the current user is already in the database
    existing_user = User.query.get(user['id'])

    if existing_user:
        User.query.delete()

    # if not add them
    ravelry_id = user['id']
    username = user['username']
    profile_img = user['photo_url']
    update_time = 14
    password =  bcrypt.using(rounds=13).hash("password")
    is_active = True
    subscribe = True
    phone_num = "5103266229"

    new_user = User(user_id=ravelry_id,
                    username=username,
                    profile_img=profile_img,
                    password=password,
                    update_time=update_time,
                    phone_num=phone_num,
                    subscribed=subscribe)

    db.session.add(new_user)

    db.session.commit()


def load_status():
    """ load status options into the database """

    # remove any existing rows in status table
    Status.query.delete()

    # get the status json from the API
    status_json = requests.get("https://api.ravelry.com/" +
                               "projects/project_statuses.json",
                               auth=(os.environ['RAVELRY_ACCESS_KEY'],
                                     os.environ['RAVELRY_PERSONAL_KEY'])).json()

    statuses = status_json['project_statuses']

    # Add each status option to the db
    for status in statuses:
        status_id = status['id']
        status = status['name']

        status_opp = Status(status_id=status_id, status=status)

        db.session.add(status_opp)

    db.session.commit()


def load_projects(user, response):
    """Load projects for a user from Ravelry api into database"""

    projects = response.json()['projects']

    user_ob = User.query.filter_by(username=user).one()
    user_ob.api_tag = response.headers['ETag']

    Project.query.filter(Project.user_id == user_ob.user_id).delete()

    for project in projects:
        add_project(user, project)

    db.session.commit()


def add_project(user, project):
    """ Add a project to the db from an api generated json dictionary """

    project_id = project['id']

    # get the full project details from ravelry
    details, p_etag = api.project_details(user, project_id)
    project_details = details['project']

    user_id = project['user_id']
    name = project['name']
    pattern_name = project['pattern_name']
    status_id = project['project_status_id']
    updated_at = project['updated_at']
    started_at = project['started']
    finished_at = project['completed']
    progress = project['progress']
    rav_page = project['permalink']

    # get the project notes
    notes = project_details['notes']

    # get images
    photos = project_details['photos']

    for photo in photos:
        url = photo['medium2_url']

        image = Image(url=url, project_id=project_id)
        db.session.add(image)

    # create a project instance
    project = Project(project_id=project_id,
                      name=name,
                      pattern_name=pattern_name,
                      status_id=status_id,
                      updated_at=updated_at,
                      user_id=user_id,
                      notes=notes,
                      started_at=started_at,
                      finished_at=finished_at,
                      progress=progress,
                      rav_page=rav_page)
                      # etag=p_etag)

    # add the project to the database
    db.session.add(project)


def sync_projects(user):
    """ Update the db with any changes from the api """

    user_ob = User.query.filter_by(username=user).first()
    etag = str(user_ob.api_etag)
    headers = {'If-None-Match': etag}
    print headers

    projects_response = api.projects(user, headers)

    print projects_response.status_code

    if projects_response.status_code == 304:

        return "No API updates"

    # if there are updates from the api
    elif projects_response.status_code == 200:

        # update the users api_etag to the new tag
        new_etag = projects_response.headers['ETag']
        print new_etag

        user_ob.api_etag = new_etag

        # get the projects dictionary list from the response
        projects = projects_response.json()['projects']

        # get the current projects for the user
        current = db.session.query(Project.project_id,
                                   Project).join(User).filter(
                                   User.username == user).all()

        # create a dict where keys are project id and value is project object
        current_projects = dict(current)

        for project in projects:
            project_id = project['id']

            # check if project is already in db
            if project_id in current_projects.keys():
                updated_at_str = project['updated_at'][:-6]
                updated_at_dt = datetime.datetime.strptime(updated_at_str, '%Y/%m/%d %X')

                # check if project has been updated on ravelry
                if updated_at_dt != current_projects[project_id].updated_at:
                    current_project = current_projects[project_id]
                    db.session.delete(current_project)
                    db.session.commit()

                    add_project(user, project)

            # if project is not in the database add it
            else:
                add_project(user, project)

        db.session.commit()

        return "database updated"

    else:
        return "API Error"


if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    load_user()
    # load_status()
    # projects_response = api.projects('zo1414')
    # load_projects('zo1414', projects_response)
    # sync_projects('zo1414')
