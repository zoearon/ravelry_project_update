from model import connect_to_db, db, User, Project, Status, Image
import datetime
import requests
import os

def update_projects(user):
    """Load projects for a user from Ravelry api into database"""

    # change to only get wips
    projects_json = requests.get('https://api.ravelry.com/projects/' + user +
                                '/list.json',
                                auth=(os.environ['RAVELRY_ACCESS_KEY'],
                                os.environ['RAVELRY_PERSONAL_KEY'])).json()

    projects = projects_json['projects']

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

        # get the full project details from ravelry
        details = requests.get('https://api.ravelry.com/projects/%s/%s.json' % (
                                user, project_id),
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

        # create a project instance
        project = Project(project_id=project_id,
                          name=name,
                          pattern_name=pattern_name,
                          status_id=status_id,
                          updated_at=updated_at,
                          user_id=user_id,
                          notes=notes,
                          started_at=started_at,
                          finished_at=finished_at)

# possible eager load
        current_project = Project.query.get(project_id)

        current_dict = current_project.__dict__
        del current_dict['_sa_instance_state']

        
        if current_dict:
            if current_project = project:
                pass
            else:
                for key in         

        else:
            # add the project to the database
            db.session.add(project)

    db.session.commit()



if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
