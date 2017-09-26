from model import connect_to_db, db, User, Project, Status, Image
import datetime
import requests
import os

def load_user():
    """ Add the current user to the database"""

    user_json = requests.get("https://api.ravelry.com/current_user.json",
                             auth=(os.environ['RAVELRY_ACCESS_KEY'],
                             os.environ['RAVELRY_PERSONAL_KEY'])).json()

    user = user_json['user']

    existing_user = User.query.get(user['id'])
    if existing_user:
        pass
    else:
        ravelry_id = user['id']
        username = user['username']
        profile_img = user['small_photo_url']

        new_user = User(user_id=ravelry_id,
                        username=username,
                        profile_img=profile_img)

        db.session.add(new_user)

    db.session.commit()

def load_status():
    """ load status options into the database """

    status_json = requests.get("https://api.ravelry.com/" +
                               "projects/project_statuses.json",
                               auth=(os.environ['RAVELRY_ACCESS_KEY'],
                               os.environ['RAVELRY_PERSONAL_KEY'])).json()

    statuses = status_json['project_statuses']

    for status in statuses:
        status_id = status['id']
        status = status['name']

        status_opp = Status(status_id=status_id, status=status)

        db.session.add(status_opp)

    db.session.commit()

def load_projects(user):
    """Load projects for a user from Ravelry api into database"""

    projects_json = requests.get('https://api.ravelry.com/projects/' + user +
                                '/list.json',
                                auth=(os.environ['RAVELRY_ACCESS_KEY'],
                                os.environ['RAVELRY_PERSONAL_KEY'])).json()

    projects = projects_json['projects']

    Project.query.delete()

    for project in projects:
        project_id = project['id']
        name = project['name']
        pattern_name = project['pattern_name']
        status_id = project['project_status_id']
        updated_at = project['updated_at']
        user_id = project['user_id']
        photos = project['photos_count']

        # check if the project is a WIP (ravelry status codefor WIP is 1)
        if status_id == 1 or photos > 0:
            # get the full project details from ravelry
            details = requests.get('https://api.ravelry.com/projects/%s/%s.json' % (user, project_id),
                                auth=(os.environ['RAVELRY_ACCESS_KEY'],
                                os.environ['RAVELRY_PERSONAL_KEY'])).json()

            project_details = details['project']
            # get the project notes
            notes = project_details['notes']

            # get images
            photos = project_details['photos']

            for photo in photos:
                url = photo['square_url']

                image = Image(url=url, project_id=project_id)
                db.session.add(image)

        else:
            # if not a WIP don't collect notes
            # Done to limmit number of API requests
            notes = "Notes are only available on curent works in progress"

        # create a project instance
        project = Project(project_id=project_id,
                          name=name,
                          pattern_name=pattern_name,
                          status_id=status_id,
                          updated_at=updated_at,
                          user_id=user_id,
                          notes=notes)

        # add the project to the database
        db.session.add(project)

    db.session.commit()



if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()



    load_user()
    load_status()
    load_projects('zo1414')