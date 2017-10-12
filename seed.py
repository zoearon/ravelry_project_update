from model import connect_to_db, db, User, Project, Status, Image
import datetime
import requests
import os
import api

def load_user():
    """ Add the current user to the database"""

    user_json = requests.get("https://api.ravelry.com/current_user.json",
                             auth=(os.environ['RAVELRY_ACCESS_KEY'],
                             os.environ['RAVELRY_PERSONAL_KEY'])).json()
    
    user = user_json['user']

    # check if the current user is already in the database
    existing_user = User.query.get(user['id'])
    
    if existing_user:
        pass
    
    # if not add them
    else:
        ravelry_id = user['id']
        username = user['username']
        profile_img = user['photo_url']
        update_time = 14
        password = "password"
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

etag = ""

def load_projects(user, response):
    """Load projects for a user from Ravelry api into database"""

    projects = response.json()['projects']
    etag = response.headers['ETag']

    Project.query.join(User).filter(User.username == user).delete()

    for project in projects:
        project_id = project['id']
        user_id = project['user_id']
        name = project['name']
        pattern_name = project['pattern_name']
        status_id = project['project_status_id']
        updated_at = project['updated_at']
        started_at = project['started']
        finished_at = project['completed']
        photos_count = project['photos_count']
        progress = project['progress']
        rav_page = project['permalink']

        # get the full project details from ravelry
        details = api.project_details(user, project_id)
        project_details = details['project']
        
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

        # add the project to the database
        db.session.add(project)

    db.session.commit()

def sync_projects(user):
    """ Update the db with any changes from the api """

    headers = {'If-None-Match': etag}

    projects_response = api.projects(user, headers)

    if projects_response.status = 304:
        pass
    elif projects_response.status = 200:
        load_projects(user, projects_response)


if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    load_user()
    load_status()
    projects_response = api.projects('zo1414')
    load_projects('zo1414')


